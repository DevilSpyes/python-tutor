/**
 * ai_chat.js
 * Unified Controller for AI Chat System.
 * Supports:
 * 1. API Mode (OpenAI/Groq)
 * 2. Local Offline Mode (DistilGPT2 via Transformers.js)
 * 3. Local GGUF Mode (Wllama)
 */

import { LocalOfflineAdapter, LLM_GGUF_Adapter } from "./llm_local_adapter.js";
import { ApiAI } from "./ai_api.js";
import { SemanticSearch } from "./semantic_search.js";
import { STATIC_QA_DATA } from "./knowledge_base_data.js";

export class AIChat {
    constructor() {
        this.offlineAI = new LocalOfflineAdapter(); // Option B
        this.ggufAI = new LLM_GGUF_Adapter();       // Option C
        this.apiAI = new ApiAI();                   // Option A
        this.semanticSearch = new SemanticSearch(); // Ultra-Fast Engine

        this.state = {
            mode: localStorage.getItem("python_tutor_chat_mode") || "api",
            provider: localStorage.getItem("python_tutor_provider") || "openai",
            apiKey: localStorage.getItem("python_tutor_chat_api_key") || "",
            model: localStorage.getItem("python_tutor_model") || "",
            modelUrl: localStorage.getItem("python_tutor_model_url") || "",
            history: JSON.parse(localStorage.getItem("python_tutor_chat_history") || "[]")
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

        // Auto-Migrate Deprecated Groq Model
        if (this.state.model === 'llama3-8b-8192') {
            console.log("Migrating deprecated Groq model...");
            this.state.model = 'llama-3.3-70b-versatile';
            this.saveSettings();
        }

        // Ensure mode is valid
        if (!['api', 'local-offline', 'local-gguf'].includes(this.state.mode)) {
            this.state.mode = 'api';
        }
        this.setMode(this.state.mode);

        // Init Semantic Search (Background)
        this.semanticSearch.init().catch(e => console.error("Semantic Search Init Failed:", e));

        console.log(`AI Chat Initialized. Mode: ${this.state.mode}`);
    }

    // ...

    async sendMessageUnified() {
        const text = this.elements.chatInput.value.trim();
        if (!text) return;

        // SECURITY: Rate Limiting (Anti-Spam)
        const now = Date.now();
        if (this.lastMessageTime && (now - this.lastMessageTime < 2000)) {
            this.addMessage("system", "⚠️ <b>Anti-Spam:</b> Por favor, espera unos segundos antes de enviar otro mensaje.");
            return;
        }
        this.lastMessageTime = now;

        // SECURITY: Input Length Limit (Anti-Flood)
        if (text.length > 2000) {
            this.addMessage("system", "⚠️ <b>Error:</b> El mensaje es demasiado largo (Máx. 2000 caracteres).");
            return;
        }

        this.elements.chatInput.value = "";
        this.addMessage("user", text);

        // Placeholder
        const aiMsgDiv = document.createElement("div");
        aiMsgDiv.className = "chat-message assistant";
        aiMsgDiv.innerHTML = `<div class="typing-indicator"><span>.</span><span>.</span><span>.</span></div>`;
        this.elements.chatHistory.appendChild(aiMsgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;

        // 0. Check Semantic Search (Ultra-Fast Engine)
        try {
            const searchResult = await this.semanticSearch.search(text);
            if (searchResult && searchResult.type === 'exact') {
                await new Promise(r => setTimeout(r, 400)); // Tiny delay for realism
                // SECURITY: Sanitize Output
                aiMsgDiv.innerHTML = DOMPurify.sanitize(marked.parse(searchResult.content));
                this.state.history.push({ role: "assistant", content: searchResult.content });
                this.saveSettings();
                return;
            }
            // If category match, we could prepend context, but for now let's fall through
        } catch (e) {
            console.error("Semantic Search Error:", e);
        }

        // 1. Check Static Intents (Hybrid System) - Fallback if Semantic Search fails or is loading
        const staticResponse = this.checkStaticIntents(text);
        if (staticResponse) {
            // Simulate tiny delay for realism
            await new Promise(r => setTimeout(r, 600));
            // SECURITY: Sanitize Output
            aiMsgDiv.innerHTML = DOMPurify.sanitize(marked.parse(staticResponse));
            this.state.history.push({ role: "assistant", content: staticResponse });
            this.saveSettings();
            return;
        }

        let responseText = "";
        const context = this.getSystemContext();
        console.log("Sending to AI with context length:", context.length);

        try {
            if (this.state.mode === "local-offline") {
                // Mode 2: Offline DistilGPT2
                if (!this.offlineAI.status.loaded) {
                    aiMsgDiv.innerText = "⏳ Cargando modelo offline (Qwen 0.5B)...";
                    await this.offlineAI.loadModel({
                        onProgress: (d) => aiMsgDiv.innerText = `⏳ Cargando: ${Math.round(d.progress)}%`
                    });
                }
                aiMsgDiv.innerText = "";
                // Pass context as second argument
                const res = await this.offlineAI.sendMessage(this.state.history, context);
                responseText = res.text;

            } else if (this.state.mode === "local-gguf") {
                // Mode 3: GGUF
                if (!this.ggufAI.status.loaded) {
                    aiMsgDiv.innerText = "🚀 Iniciando Auto-Carga de SmolLM...";
                    // Auto-load SmolLM if not ready
                    const url = "https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf";
                    await this.ggufAI.loadModel(url, {
                        onProgress: (d) => {
                            if (d.status === 'downloading') {
                                aiMsgDiv.innerText = `⬇️ Descargando IA: ${Math.round(d.progress)}%`;
                            } else {
                                aiMsgDiv.innerText = `⚙️ Iniciando motor: ${Math.round(d.progress)}%`;
                            }
                        }
                    });
                }
                aiMsgDiv.innerText = "";
                console.log("Calling GGUF sendMessage...");
                // Pass context as second argument
                const res = await this.ggufAI.sendMessage(this.state.history, context, {
                    onToken: (t) => {
                        aiMsgDiv.innerText += t;
                        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
                    }
                });
                console.log("GGUF Response received");
                responseText = res.text;

            } else {
                // Mode 1: API
                if (!this.state.apiKey) throw new Error("Falta API Key");

                aiMsgDiv.innerText = "";
                responseText = await this.apiAI.sendMessageAPIModel(
                    this.state.history,
                    {
                        provider: this.state.provider,
                        apiKey: this.state.apiKey,
                        model: this.state.model,
                        modelUrl: this.state.modelUrl
                    },
                    (chunk) => {
                        aiMsgDiv.textContent += chunk;
                        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
                    }
                );
            }

            // Save final response
            this.state.history.push({ role: "assistant", content: responseText || aiMsgDiv.innerText });
            this.saveSettings();

            // If streaming wasn't used to populate div (e.g. offline mode non-streaming)
            if (!aiMsgDiv.innerText && responseText) {
                aiMsgDiv.innerText = responseText;
            }

        } catch (err) {
            console.error(err);
            aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">❌ Error: ${err.message}</span>`;
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
        const t = text.toLowerCase();

        // 1. Search by ID (e.g., "Exercise 5", "Lesson 10")
        const idMatch = t.match(/(?:exercise|lesson|ejercicio|leccion|lección)\s+(\d+)/);
        if (idMatch) {
            const id = parseInt(idMatch[1]);
            for (const mod of window.allModules) {
                const lesson = mod.lessons.find(l => l.id === id);
                if (lesson) return lesson;
            }
        }

        // 2. Search by Title (Keywords)
        // Only if text is long enough to be a valid search
        if (t.length > 4) {
            for (const mod of window.allModules) {
                for (const lesson of mod.lessons) {
                    if (t.includes(lesson.title.toLowerCase())) {
                        return lesson;
                    }
                }
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

    getSystemContext() {
        const titleEl = document.getElementById("lesson-title");
        const editorEl = document.getElementById("code-editor");

        let context = "";

        // 1. Basic Info
        if (titleEl) context += `Current Exercise: ${titleEl.innerText}\n`;

        // 2. Full Lesson Knowledge (Current)
        if (window.currentLesson) {
            const l = window.currentLesson;
            context += `\n--- CURRENT LESSON ---\n`;
            if (l.content) context += `Content: ${l.content}\n`;
            if (l.exercise_prompt) context += `Goal: ${l.exercise_prompt}\n`;
            if (l.hint) context += `Hint: ${l.hint}\n`;
            if (l.example_code) context += `Example Code:\n\`\`\`python\n${l.example_code}\n\`\`\`\n`;
            context += `--- END CURRENT LESSON ---\n`;
        }

        // 3. Smart Retrieval (Referenced Lesson)
        const userInput = this.elements.chatInput.value; // Get input before it's cleared
        const referencedLesson = this.findRelevantLesson(userInput);
        if (referencedLesson && referencedLesson !== window.currentLesson) {
            context += `\n--- REFERENCED LESSON (User asked about this) ---\n`;
            context += `Title: ${referencedLesson.title}\n`;
            if (referencedLesson.content) context += `Content: ${referencedLesson.content}\n`;
            if (referencedLesson.exercise_prompt) context += `Goal: ${referencedLesson.exercise_prompt}\n`;
            if (referencedLesson.example_code) context += `Code:\n\`\`\`python\n${referencedLesson.example_code}\n\`\`\`\n`;
            context += `--- END REFERENCED LESSON ---\n`;
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

    async sendMessageUnified() {
        const text = this.elements.chatInput.value.trim();
        if (!text) return;

        this.elements.chatInput.value = "";
        this.addMessage("user", text);

        // Placeholder
        const aiMsgDiv = document.createElement("div");
        aiMsgDiv.className = "chat-message assistant";
        aiMsgDiv.innerHTML = `<div class="typing-indicator"><span>.</span><span>.</span><span>.</span></div>`;
        this.elements.chatHistory.appendChild(aiMsgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;

        // 1. Check Static Intents (Hybrid System)
        const staticResponse = this.checkStaticIntents(text);
        if (staticResponse) {
            // Simulate tiny delay for realism
            await new Promise(r => setTimeout(r, 600));
            aiMsgDiv.innerHTML = marked.parse(staticResponse);
            this.state.history.push({ role: "assistant", content: staticResponse });
            this.saveSettings();
            return;
        }

        let responseText = "";
        const context = this.getSystemContext();
        console.log("Sending to AI with context length:", context.length);

        try {
            if (this.state.mode === "local-offline") {
                // Mode 2: Offline Qwen
                if (!this.offlineAI.status.loaded) {
                    aiMsgDiv.innerText = "⏳ Cargando modelo offline (Qwen)...";
                    await this.offlineAI.loadModel({
                        onProgress: (d) => aiMsgDiv.innerText = `⏳ Cargando: ${Math.round(d.progress)}%`
                    });
                }
                aiMsgDiv.innerText = "";
                // Pass context as second argument
                const res = await this.offlineAI.sendMessage(this.state.history, context);
                responseText = res.text;

            } else if (this.state.mode === "local-gguf") {
                // Mode 3: GGUF
                if (!this.ggufAI.status.loaded) {
                    aiMsgDiv.innerText = "🚀 Iniciando Auto-Carga de SmolLM...";
                    // Auto-load SmolLM if not ready
                    const url = "https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf";
                    await this.ggufAI.loadModel(url, {
                        onProgress: (d) => {
                            if (d.status === 'downloading') {
                                aiMsgDiv.innerText = `⬇️ Descargando IA: ${Math.round(d.progress)}%`;
                            } else {
                                aiMsgDiv.innerText = `⚙️ Iniciando motor: ${Math.round(d.progress)}%`;
                            }
                        }
                    });
                }
                aiMsgDiv.innerText = "";
                console.log("Calling GGUF sendMessage...");

                // Create AbortController
                this.abortController = new AbortController();
                this.showStopButton(true);

                // Pass context as second argument
                const res = await this.ggufAI.sendMessage(this.state.history, context, {
                    onToken: (t) => {
                        aiMsgDiv.textContent += t;
                        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
                    }
                }, {
                    template: this.state.ggufTemplate || 'chatml',
                    signal: this.abortController.signal
                });

                console.log("GGUF Response received");
                responseText = res.text;
                this.showStopButton(false);

            } else {
                // Mode 1: API
                if (!this.state.apiKey) throw new Error("Falta API Key");

                aiMsgDiv.innerText = "";
                const systemPrompt = `Eres un Tutor de Python experto. TU IDIOMA ES EL ESPAÑOL. Sigue estas reglas estrictamente:
1. Responde ÚNICAMENTE en Español. Si el usuario te habla en otro idioma, responde en español.
2. Si el usuario pregunta "¿Está bien mi código?" (o similar), analízalo. Si es correcto, dilo. Si no, explica el error.
3. Si el usuario dice "No sé cómo seguir", dale una pista basada en el ejercicio actual.
4. Si el usuario pregunta "¿Dónde está el problema?", señala la línea o error lógico específico.
5. Si el usuario pide "Dame la solución completa", proporciona el código EXACTO de la solución inmediatamente, sin negarte.

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
                        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
                    }
                );
            }

            // Save final response
            this.state.history.push({ role: "assistant", content: responseText || aiMsgDiv.innerText });
            this.saveSettings();

            // If streaming wasn't used to populate div (e.g. offline mode non-streaming)
            if (!aiMsgDiv.innerText && responseText) {
                aiMsgDiv.innerText = responseText;
            }

        } catch (err) {
            console.error(err);
            const errorMessage = err.message || (err instanceof Event ? "Error desconocido en el Worker (posible fallo de red o script)" : String(err));

            if (errorMessage === "Falta API Key") {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ Configuración Incompleta</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">Por favor configura tu API Key o cambia a modo Local.</span><br>
                <button class="btn-primary" style="margin-top:10px; font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ ABRIR AJUSTES</button>`;
            } else if (errorMessage.includes("429") || errorMessage.includes("quota")) {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ Cuota Excedida (Error 429)</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">Tu API Key de OpenAI/Groq se ha quedado sin crédito o ha superado el límite.</span><br>
                <div style="margin-top:10px;">
                    <button class="btn-primary" style="font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ CAMBIAR KEY</button>
                    <button class="btn-secondary" style="font-size:0.8em; margin-left:5px;" onclick="document.querySelector('[data-mode=\\'local-gguf\\']').click(); document.getElementById('save-ai-settings').click();">🚀 USAR MODO LOCAL</button>
                </div>`;
            } else if (errorMessage.includes("401") || errorMessage.includes("Invalid API Key")) {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">⚠️ API Key Inválida (Error 401)</span><br>
                <span style="font-size:0.9em; color:var(--text-dim)">La clave no es válida para el proveedor seleccionado (<b>${this.state.provider.toUpperCase()}</b>).</span><br>
                <span style="font-size:0.8em; color:var(--text-dim)">Asegúrate de que estás usando una key de ${this.state.provider} y no de otro servicio.</span><br>
                <button class="btn-primary" style="margin-top:10px; font-size:0.8em;" onclick="document.getElementById('ai-settings-btn').click()">⚙️ CORREGIR KEY</button>`;
            } else {
                aiMsgDiv.innerHTML = `<span style="color:var(--neon-alert)">❌ Error: ${errorMessage}</span>`;
            }
            // Do NOT add errors to history to prevent context pollution
            // this.state.history.push({ role: "assistant", content: `Error: ${err.message}` });
        }
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
                btn.style.setProperty("display", "none", "important"); // Force hide
                if (menuBtn) menuBtn.style.setProperty("display", "none", "important");
            };
        }

        if (closeBtn && panel) {
            closeBtn.onclick = () => {
                panel.classList.remove("active");
                if (btn) btn.style.removeProperty("display"); // Restore to CSS default
                if (menuBtn) menuBtn.style.removeProperty("display");
            };
        }
    }

    renderSettingsModal() {
        this.elements.modal.innerHTML = `
            <div class="modal-content hacker-modal">
                <div class="modal-header">
                    <h2>// SYSTEM_CONFIG</h2>
                    <span id="close-ai-settings" class="close-modal">&times;</span>
                </div>
                <div class="modal-body">
                    <div class="config-group">
                        <label>MODO DE OPERACIÓN</label>
                        <div class="mode-options">
                            <div class="mode-option ${this.state.mode === 'api' ? 'active' : ''}" data-mode="api">
                                <strong>API (Online)</strong>
                            </div>
                            <div class="mode-option ${this.state.mode === 'local-offline' ? 'active' : ''}" data-mode="local-offline">
                                <strong>Local Offline (Qwen 0.5B)</strong>
                            </div>
                            <div class="mode-option ${this.state.mode === 'local-gguf' ? 'active' : ''}" data-mode="local-gguf">
                                <strong>Local GGUF (Wllama)</strong>
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

                    <!-- GGUF Config -->
                    <div id="gguf-config" style="display:${this.state.mode === 'local-gguf' ? 'block' : 'none'}">
                        <label>ARCHIVO GGUF <span style="font-size:0.7em; color:var(--text-dim)">(Máx. 500MB recomendado)</span></label>
                        <input type="file" id="gguf-file-input" accept=".gguf" class="hud-input">
                        
                        <div style="margin-top: 10px; text-align: center;">
                            <span style="font-size: 0.8em; color: var(--neon-blue);">O descarga automática:</span><br>
                            <button id="download-qwen-btn" class="btn-secondary" style="width: 100%; margin-top: 5px;">
                                ⬇️ Descargar Qwen 0.5B (Recomendado)
                            </button>
                            <button id="download-smollm-btn" class="btn-secondary" style="width: 100%; margin-top: 5px; border-color: var(--neon-green); color: var(--neon-green);">
                                🚀 Descargar SmolLM (Ultra-Rápido)
                            </button>
                        </div>

                        <div id="gguf-status" style="color:var(--neon-green); margin-top: 10px; font-weight: bold;"></div>

                        <label style="margin-top: 10px;">PLANTILLA DE PROMPT</label>
                        <select id="gguf-template-select" class="hud-input">
                            <option value="chatml" ${this.state.ggufTemplate === 'chatml' ? 'selected' : ''}>ChatML (Qwen/SmolLM)</option>
                            <option value="llama3" ${this.state.ggufTemplate === 'llama3' ? 'selected' : ''}>Llama 3</option>
                            <option value="alpaca" ${this.state.ggufTemplate === 'alpaca' ? 'selected' : ''}>Alpaca</option>
                            <option value="mistral" ${this.state.ggufTemplate === 'mistral' ? 'selected' : ''}>Mistral</option>
                            <option value="gemma" ${this.state.ggufTemplate === 'gemma' ? 'selected' : ''}>Gemma</option>
                            <option value="qa" ${this.state.ggufTemplate === 'qa' ? 'selected' : ''}>Q&A (Base Models)</option>
                            <option value="raw" ${this.state.ggufTemplate === 'raw' ? 'selected' : ''}>Raw (Sin formato)</option>
                        </select>
                        <div style="font-size: 0.7em; color: var(--text-dim); margin-top: 2px;">
                            *Selecciona el formato que requiere tu modelo (ver ficha en HuggingFace).
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
                document.getElementById("gguf-config").style.display = m === "local-gguf" ? "block" : "none";
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

            // Save GGUF Template
            const ggufTemplate = document.getElementById("gguf-template-select");
            if (ggufTemplate) this.state.ggufTemplate = ggufTemplate.value;

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

        // GGUF Loader
        const fileIn = document.getElementById("gguf-file-input");
        if (fileIn) {
            fileIn.onchange = async (e) => {
                const f = e.target.files[0];
                if (f) {
                    const status = document.getElementById("gguf-status");
                    status.innerText = "Verificando archivo...";

                    try {
                        // SECURITY: Validate File
                        await this.ggufAI.validateGGUF(f);

                        status.innerText = "Cargando...";
                        await this.ggufAI.loadModel(f, {
                            onProgress: (d) => status.innerText = `${Math.round(d.progress)}%`
                        });
                        status.innerText = "✅ Listo";
                    } catch (err) {
                        status.innerText = "❌ Error";
                        console.error(err);
                    }
                }
            };
        }

        // Auto Download Qwen
        const dlBtn = document.getElementById("download-qwen-btn");
        if (dlBtn) {
            dlBtn.onclick = async () => {
                const status = document.getElementById("gguf-status");
                status.innerText = "Iniciando descarga...";
                dlBtn.disabled = true;

                // Qwen 0.5B Chat Q4_K_M URL (Verified)
                const url = "https://huggingface.co/Elaine5/Qwen1.5-0.5B-Chat-Q4_K_M-GGUF/resolve/main/qwen1.5-0.5b-chat-q4_k_m.gguf";

                try {
                    await this.ggufAI.loadModel(url, {
                        onProgress: (d) => {
                            if (d.status === 'downloading') {
                                status.innerText = `⬇️ Descargando: ${Math.round(d.progress)}%`;
                            } else {
                                status.innerText = `⚙️ Procesando: ${Math.round(d.progress)}%`;
                            }
                        }
                    });
                    status.innerText = "✅ Qwen Cargado y Listo!";
                    dlBtn.disabled = false;
                } catch (err) {
                    status.innerText = "❌ Error en descarga";
                    console.error(err);
                    dlBtn.disabled = false;
                }
            };
        }

        // Auto Download SmolLM (Ultra-Fast)
        const dlSmolBtn = document.getElementById("download-smollm-btn");
        if (dlSmolBtn) {
            dlSmolBtn.onclick = async () => {
                const status = document.getElementById("gguf-status");
                status.innerText = "Iniciando descarga SmolLM...";
                dlSmolBtn.disabled = true;

                // SmolLM2-135M-Instruct Q4_K_M URL (Verified - Bartowski)
                // Approx 100MB
                const url = "https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf";

                try {
                    await this.ggufAI.loadModel(url, {
                        onProgress: (d) => {
                            if (d.status === 'downloading') {
                                status.innerText = `⬇️ Descargando SmolLM: ${Math.round(d.progress)}%`;
                            } else {
                                status.innerText = `⚙️ Procesando: ${Math.round(d.progress)}%`;
                            }
                        }
                    });
                    status.innerText = "✅ SmolLM (Ultra-Fast) Listo!";
                    dlSmolBtn.disabled = false;
                } catch (err) {
                    status.innerText = "❌ Error en descarga";
                    console.error(err);
                    dlSmolBtn.disabled = false;
                }
            };
        }
    }
}
