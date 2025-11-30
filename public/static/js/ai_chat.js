/**
 * ai_chat.js
 * Unified Controller for AI Chat System.
 * Supports:
 * 1. API Mode (OpenAI/Groq)
 * 2. Local Offline Mode (DistilGPT2 via Transformers.js)
 * 3. Local GGUF Mode (Wllama)
 */

import { ProfessorLiteAdapter } from "./llm_local_adapter.js";
import { ApiAI } from "./ai_api.js";
import { SemanticSearch } from "./semantic_search.js";
import { STATIC_QA_DATA } from "./knowledge_base_data.js";


const MODULE_SUMMARIES = {
    "00": "Módulo 00: Bienvenida y Guía. Configuración del entorno, filosofía del curso y primeros pasos en el sistema.",
    "01": "Módulo 01: Introducción a Python. Sintaxis básica, variables, tipos de datos (int, float, str, bool) y entrada/salida (print, input).",
    "02": "Módulo 02: Conceptos Fundamentales. Operadores aritméticos, lógicos y de comparación. Estructuras de control (if, else, elif) y bucles básicos.",
    "03": "Módulo 03: Práctica de Algoritmos. Lógica de programación, resolución de problemas, listas, diccionarios y estructuras de datos más complejas.",
    "04": "Módulo 04: Automatización y Scripts. Creación de scripts útiles, manejo de archivos, interacción con el sistema operativo y librerías estándar.",
    "05": "Módulo 05: Ciberseguridad y Criptografía. Conceptos de seguridad, encriptación, hashing y análisis de vulnerabilidades básicos con Python.",
    "06": "Módulo 06: Proyectos Finales. Desarrollo de herramientas completas de seguridad (escáneres, keyloggers educativos, etc.) y consolidación de conocimientos.",
    "07": "Módulo 07: Certificación. Evaluación final y cierre del curso."
};

export class AIChat {
    constructor() {
        this.professorLite = new ProfessorLiteAdapter();
        this.apiAI = new ApiAI();                   // Option A (Restored)
        this.semanticSearch = new SemanticSearch(); // Ultra-Fast Engine

        this.state = {
            mode: localStorage.getItem("python_tutor_chat_mode") || "professor-lite",
            provider: localStorage.getItem("python_tutor_provider") || "openai",
            apiKey: localStorage.getItem("python_tutor_chat_api_key") || "",
            model: localStorage.getItem("python_tutor_model") || "",
            modelUrl: localStorage.getItem("python_tutor_model_url") || "",
            history: JSON.parse(localStorage.getItem("python_tutor_chat_history") || "[]"),
            isGenerating: false
        };

        this.elements = {
            chatHistory: document.getElementById("chat-history"),
            chatInput: document.getElementById("chat-input"),
            sendBtn: document.getElementById("send-chat"),
            settingsBtn: document.getElementById("ai-settings-btn"),
            modeBadge: document.getElementById("ai-mode-badge"),
            modal: document.getElementById("ai-settings-modal")
        };

        this.init();
    }

    async init() {
        this.renderHistory();
        this.attachEventListeners();
        this.attachMobileListeners();
        this.injectStyles(); // New styles for Stop button

        // Ensure mode is valid
        if (!['professor-lite', 'api'].includes(this.state.mode)) {
            this.state.mode = 'professor-lite';
        }
        this.setMode(this.state.mode);

        // Init Semantic Search (Background)
        this.semanticSearch.init().catch(e => console.error("Semantic Search Init Failed:", e));

        console.log(`AI Chat Initialized. Mode: ${this.state.mode}`);
    }

    // ...

    async sendMessageUnified() {
        if (this.state.isGenerating) return; // Prevent multiple clicks
        const text = this.elements.chatInput.value.trim();
        if (!text) return;

        this.state.isGenerating = true;

        this.elements.chatInput.value = "";
        this.addMessage("user", text);

        // Placeholder
        const aiMsgDiv = document.createElement("div");
        aiMsgDiv.className = "chat-message assistant";
        aiMsgDiv.innerHTML = `<div class="typing-indicator"><span>.</span><span>.</span><span>.</span></div>`;
        this.elements.chatHistory.appendChild(aiMsgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;

        let responseText = "";
        const context = this.getSystemContext(text);
        console.log("Sending to AI with context length:", context.length);

        // DEBUG COMMAND
        if (text.startsWith("DEBUG_CONTEXT")) {
            const debugQuery = text.replace("DEBUG_CONTEXT", "").trim() || text;
            const debugContext = this.getSystemContext(debugQuery);
            this.addMessage("assistant", "```text\n" + debugContext + "\n```");
            return;
        }

        let fullText = "";
        let lastUpdate = 0;

        // Helper to update UI safely
        const updateUI = (text) => {
            const history = this.elements.chatHistory;
            // Check if user is near bottom (allow 50px leeway)
            const isNearBottom = history.scrollHeight - history.scrollTop - history.clientHeight <= 50;

            aiMsgDiv.innerText = text;

            if (isNearBottom) {
                history.scrollTop = history.scrollHeight;
            }
        };

        try {
            if (this.state.mode === "professor-lite") {
                // --- PROFESSOR LITE MODE ---
                if (!this.professorLite.status.loaded) {
                    aiMsgDiv.innerText = "👨‍🏫 Profesor Lite: Preparando clase...";
                    await this.professorLite.loadModel({}, {
                        onProgress: (d) => {
                            aiMsgDiv.innerText = `👨‍🏫 ${d.message}`;
                        }
                    });
                }

                // Generate Response
                const responsePromise = this.professorLite.sendMessage(this.state.history, context, {
                    onToken: (token) => {
                        fullText += token;
                        const now = Date.now();
                        // Throttle updates to every 100ms to prevent scroll blocking
                        if (now - lastUpdate > 100) {
                            updateUI(fullText);
                            lastUpdate = now;
                        }
                    }
                });

                // Ensure final update is rendered
                responsePromise.then(() => updateUI(fullText));

                // Safety Timeout: If no response in 10s, force error
                const timeoutPromise = new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Timeout: El profesor tardó demasiado en responder.")), 10000)
                );

                const response = await Promise.race([responsePromise, timeoutPromise]);
                responseText = response.text;

            } else {
                // --- API MODE ---
                if (!this.state.apiKey) throw new Error("Falta API Key");

                aiMsgDiv.innerText = "";
                const systemPrompt = `Eres un Tutor de Python experto. TU IDIOMA ES EL ESPAÑOL. Sigue estas reglas estrictamente:
1. Responde ÚNICAMENTE en Español. Si el usuario te habla en otro idioma, responde en español.
2. Si el usuario pregunta "¿Está bien mi código?" (o similar), analízalo. Si es correcto, dilo. Si no, explica el error.
3. Si el usuario dice "No sé cómo seguir", dale una pista basada en el ejercicio actual.
4. Si el usuario pregunta "¿Dónde está el problema?", señala la línea o error lógico específico.
5. Si el usuario pide "Dame la solución completa", proporciona el código EXACTO de la solución inmediatamente, sin negarte.
6. FORMATO: Usa Markdown. Usa encabezados (##) para separar secciones. Usa listas (- ) para enumerar puntos. AÑADE SALTOS DE LÍNEA entre secciones para que el texto no se vea amontonado.

Contexto:
${context}`;

                // Use Clean History to avoid confusing the model with system errors
                const cleanHistory = this.getCleanHistory();

                responseText = await this.apiAI.sendMessageAPIModel(
                    [
                        { role: "system", content: systemPrompt },
                        ...cleanHistory
                    ],
                    {
                        provider: this.state.provider,
                        apiKey: this.state.apiKey,
                        model: this.state.model,
                        modelUrl: this.state.modelUrl
                    },
                    (chunk) => {
                        aiMsgDiv.textContent += chunk;
                        const now = Date.now();
                        if (now - lastUpdate > 100) {
                            updateUI(aiMsgDiv.textContent);
                            lastUpdate = now;
                        }
                    }
                );

                // Ensure final update
                updateUI(aiMsgDiv.textContent);
            }

            // Save final response
            this.state.history.push({ role: "assistant", content: responseText || aiMsgDiv.innerText });
            this.saveSettings();

            // If streaming wasn't used (or early return), force update
            if (responseText && (aiMsgDiv.querySelector(".typing-indicator") || !aiMsgDiv.innerText.trim())) {
                aiMsgDiv.innerText = responseText;
            }

        } catch (err) {
            console.error(err);
            const errorMessage = err.message || (err instanceof Event ? "Error desconocido" : String(err));

            if (errorMessage === "Falta API Key") {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ Configuración Incompleta</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">Por favor configura tu API Key o cambia a modo Local.</span><br>
                <button class="btn-primary" style="margin-top:10px; font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ ABRIR AJUSTES</button>`;
            } else if (errorMessage.includes("429") || errorMessage.includes("quota")) {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ Cuota Excedida (Error 429)</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">Tu API Key de OpenAI/Groq se ha quedado sin crédito o ha superado el límite.</span><br>
                <div style="margin-top:10px;">
                    <button class="btn-primary" style="font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ CAMBIAR KEY</button>
                    <button class="btn-secondary" style="font-size:0.8em; margin-left:5px;" onclick="document.querySelector('[data-mode=\\'professor-lite\\']').click(); document.getElementById('save-ai-settings').click();">👨‍🏫 USAR PROFESOR LITE</button>
                </div>`;
            } else if (errorMessage.includes("401") || errorMessage.includes("Invalid API Key")) {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ API Key Inválida (Error 401)</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">La clave no es válida para el proveedor seleccionado (<b>${this.state.provider.toUpperCase()}</b>).</span><br>
                <span style="font-size:0.8em; color:var(--text-dim)">Asegúrate de que estás usando una key de ${this.state.provider} y no de otro servicio.</span><br>
                <button class="btn-primary" style="margin-top:10px; font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ CORREGIR KEY</button>`;
            } else {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">❌ Error: ${errorMessage}</span>`;
            }
        } finally {
            this.state.isGenerating = false;
        }
    }

    saveSettings() {
        localStorage.setItem("python_tutor_chat_mode", this.state.mode);
        localStorage.setItem("python_tutor_provider", this.state.provider);
        localStorage.setItem("python_tutor_chat_api_key", this.state.apiKey);
        localStorage.setItem("python_tutor_model", this.state.model);
        localStorage.setItem("python_tutor_model_url", this.state.modelUrl);
        localStorage.setItem("python_tutor_chat_history", JSON.stringify(this.state.history));
    }

    setMode(mode) {
        this.state.mode = mode;
        this.saveSettings();
        // Update UI if needed (badges, etc)
    }

    addMessage(role, content) {
        this.state.history.push({ role, content });
        this.saveSettings();
        this.renderMessage(role, content);
    }

    clearHistory() {
        this.state.history = [];
        this.saveSettings();
        this.renderHistory();
    }

    renderHistory() {
        if (!this.elements.chatHistory) return;
        this.elements.chatHistory.innerHTML = "";
        this.state.history.forEach(msg => this.renderMessage(msg.role, msg.content));
    }

    renderMessage(role, content) {
        if (!this.elements.chatHistory) return;
        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-message ${role}`;

        // Basic formatting
        if (content.includes("```")) {
            const parts = content.split("```");
            parts.forEach((part, i) => {
                if (i % 2 === 1) {
                    const pre = document.createElement("pre");
                    pre.innerText = part;
                    msgDiv.appendChild(pre);
                } else {
                    const span = document.createElement("span");
                    span.innerText = part;
                    msgDiv.appendChild(span);
                }
            });
        } else {
            msgDiv.innerText = content;
        }

        this.elements.chatHistory.appendChild(msgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
    }

    showWelcomeMessage() {
        if (this.state.history.length === 0) {
            this.addMessage("system", "Sistema AI Online. Listo para ayudarte con Python.");
        }
    }

    findRelevantLesson(text) {
        if (!window.allModules) return null;

        const normalize = (str) => str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        const t = normalize(text);

        // 1. Search by ID (e.g., "Exercise 5", "Lesson 10")
        const idMatch = t.match(/(?:exercise|lesson|ejercicio|leccion|leccion)\s+(\d+)/);
        if (idMatch) {
            const id = parseInt(idMatch[1]);
            for (const mod of window.allModules) {
                const lesson = mod.lessons.find(l => l.id === id);
                if (lesson) return lesson;
            }
        }

        // 2. Search by Title (Keywords & Fuzzy)
        if (t.length > 3) {
            // Extract significant words (len > 3) from user text
            const userWords = t.split(/\s+/).filter(w => w.length > 3 && !["como", "para", "este", "esta", "esto", "pero", "porque"].includes(w));
            console.log("findRelevantLesson keywords:", userWords);

            for (const mod of window.allModules) {
                for (const lesson of mod.lessons) {
                    const titleNorm = normalize(lesson.title);

                    // A. Exact substring match (User text contains Title OR Title contains User text)
                    if (t.includes(titleNorm) || titleNorm.includes(t)) {
                        console.log("findRelevantLesson match (substring):", lesson.title);
                        return lesson;
                    }

                    // B. Keyword Match (Title contains ALL significant user words)
                    // Only if we have significant words to check
                    if (userWords.length > 0) {
                        const allWordsFound = userWords.every(w => titleNorm.includes(w));
                        if (allWordsFound) {
                            console.log("findRelevantLesson match (keywords):", lesson.title);
                            return lesson;
                        }
                    }
                }
            }
        }
        return null;
    }

    findRelevantModule(text) {
        const t = text.toLowerCase();
        console.log("findRelevantModule input:", t);
        // Match "modulo X", "module X", "módulo X"
        const moduleMatch = t.match(/(?:module|modulo|módulo)\s+(\d+)/);
        if (moduleMatch) {
            const moduleId = moduleMatch[1].padStart(2, '0'); // Ensure "04" format
            console.log("findRelevantModule match:", moduleId);
            if (MODULE_SUMMARIES[moduleId]) {
                console.log("findRelevantModule found summary");
                return {
                    id: moduleId,
                    summary: MODULE_SUMMARIES[moduleId]
                };
            } else {
                console.log("findRelevantModule summary NOT found for:", moduleId);
            }
        }
        return null;
    }

    injectStyles() {
        const style = document.createElement('style');
        style.innerHTML = `
            .stop-btn {
                background: rgba(255, 0, 0, 0.2);
                border: 1px solid var(--neon-alert);
                color: var(--neon-alert);
                padding: 5px 10px;
                cursor: pointer;
                font-family: 'Fira Code', monospace;
                font-size: 0.8em;
                display: none; /* Hidden by default */
                margin-left: 10px;
            }
            .stop-btn:hover {
                background: var(--neon-alert);
                color: #000;
            }
        `;
        document.head.appendChild(style);
    }

    showStopButton(show) {
        let btn = document.getElementById("stop-chat-btn");
        if (!btn) {
            // Create if not exists (append to chat input wrapper)
            const wrapper = document.querySelector(".chat-input-wrapper");
            btn = document.createElement("button");
            btn.id = "stop-chat-btn";
            btn.className = "stop-btn";
            btn.innerText = "■ STOP";
            btn.onclick = () => this.stopGeneration();
            wrapper.insertBefore(btn, this.elements.sendBtn);
        }
        btn.style.display = show ? "inline-block" : "none";
        this.elements.sendBtn.style.display = show ? "none" : "inline-block";
    }

    stopGeneration() {
        if (this.abortController) {
            this.abortController.abort();
            this.abortController = null;
            this.addMessage("system", "🛑 Generación detenida por el usuario.");
            this.showStopButton(false);
        }
    }

    getSystemContext(userText = "") {
        const titleEl = document.getElementById("lesson-title");
        const editorEl = document.getElementById("code-editor");

        let context = "";

        // 1. Basic Info
        if (titleEl) context += `Current Exercise: ${titleEl.innerText}\n`;

        // 2. Full Lesson Knowledge (Current)
        if (window.currentLesson) {
            const l = window.currentLesson;
            context += `\n--- CURRENT LESSON (ID: ${l.id}) ---\n`;
            if (l.content) context += `Content: ${l.content}\n`;
            if (l.exercise_prompt) context += `Goal: ${l.exercise_prompt}\n`;
            if (l.hint) context += `Hint: ${l.hint}\n`;
            if (l.example_code) context += `Example Code:\n\`\`\`python\n${l.example_code}\n\`\`\`\n`;
            context += `--- END CURRENT LESSON ---\n`;
        }

        // 3. Smart Retrieval (Referenced Lesson or Module)
        // Use the passed userText instead of reading from the cleared input

        // Check for Module Query first
        const referencedModule = this.findRelevantModule(userText);
        if (referencedModule) {
            console.log("Injecting Module Summary into Context");
            context += `\n<<<MODULE_SUMMARY>>>${referencedModule.summary}<<<END_MODULE_SUMMARY>>>\n`;
        } else {
            // Fallback to Lesson Search
            const referencedLesson = this.findRelevantLesson(userText);
            if (referencedLesson && referencedLesson !== window.currentLesson) {
                console.log("Injecting Lesson Context for:", referencedLesson.title);
                context += `\n<<<REFERENCED_LESSON>>>\n`;
                context += `ID: ${referencedLesson.id}\n`;
                context += `Title: ${referencedLesson.title}\n`;
                if (referencedLesson.content) context += `Content: ${referencedLesson.content}\n`;
                if (referencedLesson.exercise_prompt) context += `Goal: ${referencedLesson.exercise_prompt}\n`;
                if (referencedLesson.example_code) context += `Code:\n\`\`\`python\n${referencedLesson.example_code}\n\`\`\`\n`;
                context += `<<<END_REFERENCED_LESSON>>>\n`;
            }
        }

        // 4. User's Current Code
        if (editorEl) context += `\nUser Code:\n\`\`\`python\n${editorEl.value}\n\`\`\`\n`;

        return context;
    }

    getCleanHistory() {
        // Filter out error messages and temporary system alerts from history
        return this.state.history.filter(msg => {
            // Keep user messages
            if (msg.role === 'user') return true;
            // Keep assistant messages that are not errors
            if (msg.role === 'assistant') {
                return !msg.content.startsWith("❌ Error:") &&
                    !msg.content.includes("Error:") &&
                    !msg.content.includes("Anti-Spam");
            }
            // Keep system messages only if they are not errors/alerts
            if (msg.role === 'system') {
                return !msg.content.startsWith("⚠️") &&
                    !msg.content.startsWith("❌") &&
                    !msg.content.includes("Error");
            }
            return true;
        });
    }

    checkStaticIntents(text) {
        // Normalize: lowercase, remove punctuation/accents, trim
        const normalize = (str) => str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[.,!¡?¿]/g, "").trim();
        const t = normalize(text);

        // 1. Check Definitive QA Pack (Instant Response)
        for (const item of STATIC_QA_DATA) {
            const q = normalize(item.q);
            // Exact match or contained (if short) or fuzzy
            if (t === q || (t.includes(q) && q.length > 5) || (q.includes(t) && t.length > 5)) {
                return item.a;
            }
        }

        // 2. Fallback: Greetings (Relaxed - includes)
        if (t.includes("hola") || t.includes("buenos dias") || t === "hi" || t === "hello") {
            return "¡Hola! Soy tu tutor de Python. Veo que estás en el ejercicio de **" + (window.currentLesson ? window.currentLesson.title : "Introducción") + "**. ¿En qué puedo ayudarte?";
        }

        // 3. Fallback: Help / What to do (Direct Knowledge Retrieval)
        // REMOVED: User prefers AI to handle explanations for better detail.
        /*
        if (t.match(/(ayuda|que hago|que tengo que hacer|no entiendo|explicame|explícame|que hay que hacer|de que va|resumirme|trata|consiste|objetivo|resume|resumen|para que sirve|para que es|que es esto)/)) {
            if (window.currentLesson) {
                // ... (Static logic removed to let AI answer) ...
            }
        }
        */

        return null; // No static match, proceed to AI
    }

    // --- UI Helpers ---

    attachEventListeners() {
        if (this.elements.sendBtn) {
            this.elements.sendBtn.onclick = () => this.sendMessageUnified();
        }
        if (this.elements.chatInput) {
            this.elements.chatInput.onkeypress = (e) => {
                if (e.key === "Enter") this.sendMessageUnified();
            };
        }

        // Global click for settings
        document.body.addEventListener("click", (e) => {
            const btn = e.target.closest("#ai-settings-btn");
            if (btn) {
                this.renderSettingsModal();
                this.elements.modal.style.display = "flex";
            }
        });
    }

    attachMobileListeners() {
        const btn = document.getElementById("mobile-ai-btn");
        const panel = document.getElementById("ai-panel");
        const closeBtn = panel ? panel.querySelector(".close-chat-btn") : null;
        const menuBtn = document.getElementById("mobile-menu-btn");

        if (btn && panel) {
            btn.onclick = () => {
                panel.classList.add("active");
                document.body.classList.add("panel-open");
                btn.style.setProperty("display", "none", "important"); // Force hide
                if (menuBtn) menuBtn.style.setProperty("display", "none", "important");
            };
        }

        if (closeBtn && panel) {
            closeBtn.onclick = () => {
                panel.classList.remove("active");
                document.body.classList.remove("panel-open");
                if (btn) btn.style.removeProperty("display"); // Restore to CSS default
                if (menuBtn) menuBtn.style.removeProperty("display");
            };
        }
    }

    renderSettingsModal() {
        this.elements.modal.innerHTML = `
            <div class="modal-content hacker-modal">
                <div class="modal-header">
                    <h2>// AJUSTES_CHAT_AI</h2>
                    <span id="close-ai-settings" class="close-modal">&times;</span>
                </div>
                <div class="modal-body">
                    <div class="config-group">
                        <label>MODO DE OPERACIÓN</label>
                        <div class="mode-selector">
                            <div class="mode-option ${this.state.mode === 'professor-lite' ? 'active' : ''}" data-mode="professor-lite">
                                <strong>👨‍🏫 Profesor Lite (Local)</strong>
                            </div>
                            <div class="mode-option ${this.state.mode === 'api' ? 'active' : ''}" data-mode="api">
                                <strong>☁️ API (Online)</strong>
                            </div>
                        </div>
                    </div>

                    <!-- API Config -->
                    <div id="api-config" style="display:${this.state.mode === 'api' ? 'block' : 'none'}">
                        <label>PROVIDER</label>
                        <select id="api-provider-select" class="hud-input">
                            <option value="openai" ${this.state.provider === 'openai' ? 'selected' : ''}>OpenAI</option>
                            <option value="groq" ${this.state.provider === 'groq' ? 'selected' : ''}>Groq</option>
                            <option value="deepseek" ${this.state.provider === 'deepseek' ? 'selected' : ''}>DeepSeek</option>
                            <option value="custom" ${this.state.provider === 'custom' ? 'selected' : ''}>Custom / Generic</option>
                        </select>

                        <div id="api-key-group">
                            <label>API KEY</label>
                            <input type="password" id="ai-api-key" class="hud-input" value="${this.state.apiKey}">
                        </div>

                        <!-- Custom Provider Fields -->
                        <div id="custom-api-fields" style="display:${this.state.provider === 'custom' ? 'block' : 'none'}; margin-top: 10px; border-top: 1px dashed #333; padding-top: 10px;">
                            <label>BASE URL (e.g. http://localhost:1234/v1/chat/completions)</label>
                            <input type="text" id="custom-model-url" class="hud-input" value="${this.state.modelUrl}" placeholder="https://api.example.com/v1/chat/completions">
                            
                            <label>MODEL NAME (Optional)</label>
                            <input type="text" id="custom-model-name" class="hud-input" value="${this.state.model}" placeholder="my-model-v1">
                        </div>
                    </div>



                    <div class="modal-actions">
                        <button id="clear-chat-history" class="btn-secondary" style="margin-right: auto; border: 1px solid var(--neon-alert); color: var(--neon-alert);">BORRAR HISTORIAL</button>
                        <button id="save-ai-settings" class="btn-primary">GUARDAR</button>
                    </div>
                </div>
            </div>
        `;

        this.attachModalLogic();
    }

    attachModalLogic() {
        // Close
        document.getElementById("close-ai-settings").onclick = () => this.elements.modal.style.display = "none";

        // Mode Switch
        const opts = this.elements.modal.querySelectorAll(".mode-option");
        opts.forEach(opt => {
            opt.onclick = () => {
                opts.forEach(o => o.classList.remove("active"));
                opt.classList.add("active");
                const m = opt.getAttribute("data-mode");

                document.getElementById("api-config").style.display = m === "api" ? "block" : "none";
            };
        });

        // Provider Change
        const provSelect = document.getElementById("api-provider-select");
        if (provSelect) {
            provSelect.onchange = () => {
                const isCustom = provSelect.value === 'custom';
                const customFields = document.getElementById("custom-api-fields");
                if (customFields) customFields.style.display = isCustom ? "block" : "none";
            };
        }

        // Save
        document.getElementById("save-ai-settings").onclick = () => {
            const active = this.elements.modal.querySelector(".mode-option.active");
            if (active) this.state.mode = active.getAttribute("data-mode");

            const key = document.getElementById("ai-api-key");
            if (key) this.state.apiKey = key.value;

            const prov = document.getElementById("api-provider-select");
            if (prov) this.state.provider = prov.value;

            // Save Custom Fields
            const modelUrl = document.getElementById("custom-model-url");
            if (modelUrl) this.state.modelUrl = modelUrl.value;

            const modelName = document.getElementById("custom-model-name");
            if (modelName) this.state.model = modelName.value;

            this.saveSettings();
            this.elements.modal.style.display = "none";
        };

        // Clear History
        const clearBtn = document.getElementById("clear-chat-history");
        if (clearBtn) {
            clearBtn.onclick = () => {
                if (confirm("¿Estás seguro de borrar el historial?")) {
                    this.clearHistory();
                    this.elements.modal.style.display = "none";
                }
            };
        }

    }
}
