/**
 * ai_chat.js
 * Unified Controller for AI Chat System.
 * Manages UI, State, and routing between Local and API modes.
 */

import { LocalAI } from "./ai_local.js";
import { ApiAI } from "./ai_api.js";
import { CpuAI } from "./ai_cpu.js";

export class AIChat {
    constructor() {
        this.localAI = new LocalAI();
        this.apiAI = new ApiAI();
        this.cpuAI = new CpuAI();

        this.state = {
            mode: localStorage.getItem("python_tutor_chat_mode") || "api", // 'local', 'cpu', 'api', 'model'
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
            sidebarSettingsBtn: document.getElementById("sidebar-settings-btn"),
            modeBadge: document.getElementById("ai-mode-badge"),
            modal: document.getElementById("ai-settings-modal")
        };

        this.init();
    }

    async init() {
        this.renderHistory();
        this.updateUI();
        this.attachEventListeners();

        // Auto-Detection Logic (Prompt 10)
        // Only run if mode hasn't been explicitly set by user preference, or if we want to enforce capabilities
        const savedMode = localStorage.getItem("python_tutor_chat_mode");

        if (!savedMode) {
            if (navigator.gpu) {
                console.log("WebGPU detected. Defaulting to Local Mode.");
                this.setMode("local");
            } else {
                console.log("WebGPU NOT detected. Defaulting to Lite (CPU) Mode.");
                this.setMode("cpu");
                this.addSystemMessage("⚠️ WebGPU no detectado. Activando Modo Lite (CPU).");
            }
        } else {
            // Validate saved mode against capabilities
            if (savedMode === "local" && !navigator.gpu) {
                this.setMode("cpu");
                this.addSystemMessage("⚠️ WebGPU no disponible. Cambiando a Modo Lite.");
            }
        }
    }

    setMode(mode) {
        this.state.mode = mode;
        localStorage.setItem("python_tutor_chat_mode", mode);
        this.updateUI();
    }

    saveSettings() {
        localStorage.setItem("python_tutor_provider", this.state.provider);
        localStorage.setItem("python_tutor_chat_api_key", this.state.apiKey);
        localStorage.setItem("python_tutor_model", this.state.model);
        localStorage.setItem("python_tutor_model_url", this.state.modelUrl);
        localStorage.setItem("python_tutor_chat_history", JSON.stringify(this.state.history));
    }

    updateUI() {
        if (this.elements.modeBadge) {
            const labels = { api: "NUBE", local: "LOCAL", model: "CUSTOM" };
            this.elements.modeBadge.innerText = labels[this.state.mode] || "API";
            this.elements.modeBadge.style.background = this.state.mode === "local" ? "#238636" : "#1f6feb";
        }
    }

    addMessage(role, content) {
        this.state.history.push({ role, content });
        this.saveSettings();
        this.renderMessage(role, content);
    }

    addSystemMessage(content) {
        const msgDiv = document.createElement("div");
        msgDiv.className = "message system";
        msgDiv.innerText = content;
        this.elements.chatHistory.appendChild(msgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
    }

    renderMessage(role, content) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${role}`;

        if (role === "ai") {
            msgDiv.innerHTML = window.marked ? window.marked.parse(content) : content;
        } else {
            msgDiv.innerText = content;
        }

        this.elements.chatHistory.appendChild(msgDiv);
        this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
        return msgDiv;
    }

    renderHistory() {
        this.elements.chatHistory.innerHTML = "";
        // Welcome message if empty
        if (this.state.history.length === 0) {
            this.addSystemMessage("¡Hola! Soy tu tutor de Python. Configúrame en los ajustes y pregúntame lo que quieras.");
        }
        this.state.history.forEach(msg => this.renderMessage(msg.role, msg.content));
    }

    async sendMessageUnified() {
        const text = this.elements.chatInput.value.trim();
        if (!text) return;

        this.elements.chatInput.value = "";
        this.addMessage("user", text);

        // Create placeholder for AI response
        const aiMsgDiv = this.renderMessage("ai", "...");
        const typingIndicator = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;
        aiMsgDiv.innerHTML = typingIndicator;

        let fullResponse = "";
        const onChunk = (chunk) => {
            fullResponse += chunk;
            aiMsgDiv.innerHTML = window.marked ? window.marked.parse(fullResponse) : fullResponse;
            this.elements.chatHistory.scrollTop = this.elements.chatHistory.scrollHeight;
        };

        try {
            if (this.state.mode === "local") {
                // Check GPU again just in case
                const hasGPU = await this.localAI.checkWebGPUSupport();
                if (!hasGPU) throw new Error("WebGPU no disponible. Cambia a modo API.");

                // Init if needed
                if (!this.localAI.isLoaded) {
                    aiMsgDiv.innerText = "⏳ Cargando modelo local (esto puede tardar)...";
                    await this.localAI.init((text, progress) => {
                        aiMsgDiv.innerText = `⏳ Cargando: ${Math.round(progress * 100)}%`;
                    });
                    aiMsgDiv.innerHTML = typingIndicator;
                }

                const messages = [
                    { role: "system", content: "Eres un tutor de Python útil y conciso." },
                    ...this.state.history.slice(-10) // Keep context small for local
                ];

                await this.localAI.sendMessageLocalModel(messages, onChunk);

            } else if (this.state.mode === "api") {
                const config = {
                    provider: this.state.provider,
                    apiKey: this.state.apiKey,
                    model: this.state.model
                };

                const messages = [
                    { role: "system", content: "Eres un tutor de Python útil y conciso." },
                    ...this.state.history
                ];

                fullResponse = await this.apiAI.sendMessageAPIModel(messages, config, onChunk);

            } else if (this.state.mode === "model") {
                const config = {
                    provider: "custom",
                    modelUrl: this.state.modelUrl
                };
                const messages = [
                    { role: "system", content: "Eres un tutor de Python útil y conciso." },
                    ...this.state.history
                ];
                fullResponse = await this.apiAI.sendMessageAPIModel(messages, config, onChunk);
            }

            // Save final response
            this.state.history.push({ role: "ai", content: fullResponse });
            this.saveSettings();

        } catch (error) {
            console.error("Chat Error:", error);
            aiMsgDiv.className = "message error";
            aiMsgDiv.innerText = `❌ Error: ${error.message}`;

            // Auto-fallback trigger on specific errors?
            if (this.state.mode === "local" && error.message.includes("WebGPU")) {
                this.setMode("api");
                this.addSystemMessage("⚠️ Fallo en modo Local. Cambiando a modo API.");
            }
        }
    }

    attachEventListeners() {
        this.elements.sendBtn.addEventListener("click", () => this.sendMessageUnified());

        // Auto-resize and Enter key
        this.elements.chatInput.addEventListener("input", () => {
            this.elements.chatInput.style.height = "auto";
            this.elements.chatInput.style.height = (this.elements.chatInput.scrollHeight) + "px";
        });

        this.elements.chatInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.sendMessageUnified();
            }
        });

        // Settings Modal Logic
        const openSettings = () => {
            this.renderSettingsModal();
            this.elements.modal.style.display = "flex";
        };

        if (this.elements.settingsBtn) this.elements.settingsBtn.addEventListener("click", openSettings);
        if (this.elements.sidebarSettingsBtn) this.elements.sidebarSettingsBtn.addEventListener("click", openSettings);

        // Close Modal (Delegation or direct if elements exist)
        this.elements.modal.addEventListener("click", (e) => {
            if (e.target === this.elements.modal) this.elements.modal.style.display = "none";
        });
    }

    renderSettingsModal() {
        this.elements.modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Configuración de Chat</h3>
                    <button id="close-ai-settings" class="icon-btn">✕</button>
                </div>
                <div class="modal-body">
                    <!-- Mode Selection -->
                    <div class="form-group">
                        <label>Modo de Operación</label>
                        <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                            <label style="cursor: pointer; display: flex; align-items: center; gap: 8px; background: #21262d; padding: 8px 12px; border-radius: 6px; border: 1px solid #30363d;">
                                <input type="radio" name="chat_mode" value="api" ${this.state.mode === 'api' ? 'checked' : ''}> 
                                <span>☁️ API Key</span>
                            </label>
                            <label style="cursor: pointer; display: flex; align-items: center; gap: 8px; background: #21262d; padding: 8px 12px; border-radius: 6px; border: 1px solid #30363d;">
                                <input type="radio" name="chat_mode" value="local" ${this.state.mode === 'local' ? 'checked' : ''}> 
                                <span>💻 Local (WebGPU)</span>
                            </label>
                            <label style="cursor: pointer; display: flex; align-items: center; gap: 8px; background: #21262d; padding: 8px 12px; border-radius: 6px; border: 1px solid #30363d;">
                                <input type="radio" name="chat_mode" value="model" ${this.state.mode === 'model' ? 'checked' : ''}> 
                                <span>🌐 Remoto</span>
                            </label>
                        </div>
                    </div>

                    <!-- API Config -->
                    <div id="api-config-group" style="display: ${this.state.mode === 'api' ? 'block' : 'none'};">
                        <div class="form-group">
                            <label>Proveedor</label>
                            <select id="ai-provider-select">
                                <option value="openai" ${this.state.provider === 'openai' ? 'selected' : ''}>OpenAI</option>
                                <option value="groq" ${this.state.provider === 'groq' ? 'selected' : ''}>Groq (Llama 3)</option>
                                <option value="deepseek" ${this.state.provider === 'deepseek' ? 'selected' : ''}>DeepSeek</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>API Key</label>
                            <input type="password" id="ai-api-key" placeholder="sk-..." value="${this.state.apiKey}">
                        </div>
                        <div class="form-group">
                            <label>Modelo (Opcional)</label>
                            <input type="text" id="ai-model-name" placeholder="Ej: gpt-4o-mini" value="${this.state.model}">
                        </div>
                        <button id="test-api-connection" class="btn-secondary" style="width: 100%;">Probar Conexión</button>
                    </div>

                    <!-- Local Config -->
                    <div id="local-config-group" style="display: ${this.state.mode === 'local' ? 'block' : 'none'};">
                        <p style="font-size: 0.9em; color: #8b949e; margin-bottom: 10px; background: #0d1117; padding: 10px; border-radius: 6px;">
                            ℹ️ Ejecuta <b>Qwen2.5-0.5B</b> en tu navegador. Requiere descarga inicial (~300MB).
                        </p>
                        <div style="background: #0d1117; padding: 10px; border-radius: 4px; border: 1px solid #30363d;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.85em; margin-bottom: 5px;">
                                <span>Estado:</span>
                                <span id="local-load-status" style="color: #2ea043;">${this.localAI.isLoaded ? 'Listo' : 'No cargado'}</span>
                            </div>
                            <div id="local-progress-bar" style="width: 100%; height: 4px; background: #30363d; border-radius: 2px; overflow: hidden;">
                                <div id="local-progress-fill" style="width: ${this.localAI.isLoaded ? '100%' : '0%'}; height: 100%; background: #2ea043;"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Remote Model Config -->
                    <div id="model-config-group" style="display: ${this.state.mode === 'model' ? 'block' : 'none'};">
                         <div class="form-group">
                            <label>URL del Modelo</label>
                            <input type="text" id="ai-model-url" placeholder="https://tu-servidor.com/v1/chat/completions" value="${this.state.modelUrl}">
                        </div>
                        <button id="test-model-connection" class="btn-secondary" style="width: 100%;">Probar Endpoint</button>
                    </div>

                    <div id="config-feedback" style="margin-top: 15px; font-size: 0.9em; min-height: 20px; text-align: center;"></div>
                    
                    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #30363d;">
                        <button id="clear-history-btn" class="btn-secondary" style="color: #ff7b72; border-color: #ff7b72; width: 100%;">🗑️ Borrar Historial</button>
                    </div>
                </div>
                <div class="modal-footer">
                    <button id="save-ai-settings" class="btn-primary">Guardar Cambios</button>
                </div>
            </div>
        `;

        // Re-attach listeners for the new modal content
        this.attachModalListeners();
    }

    attachModalListeners() {
        // Close
        document.getElementById("close-ai-settings").addEventListener("click", () => {
            this.elements.modal.style.display = "none";
        });

        // Save
        document.getElementById("save-ai-settings").addEventListener("click", () => {
            const rbs = document.getElementsByName("chat_mode");
            for (const rb of rbs) {
                if (rb.checked) this.state.mode = rb.value;
            }

            const apiGroup = document.getElementById("api-config-group");
            if (apiGroup) {
                this.state.provider = document.getElementById("ai-provider-select").value;
                this.state.apiKey = document.getElementById("ai-api-key").value;
                this.state.model = document.getElementById("ai-model-name").value;
            }

            const modelGroup = document.getElementById("model-config-group");
            if (modelGroup) {
                this.state.modelUrl = document.getElementById("ai-model-url").value;
            }

            this.saveSettings();
            this.setMode(this.state.mode);
            this.elements.modal.style.display = "none";

            if (this.state.mode === "local") {
                this.localAI.checkWebGPUSupport().then(supported => {
                    if (!supported) {
                        alert("Tu navegador no soporta WebGPU. Se usará modo API.");
                        this.setMode("api");
                    }
                });
            }
        });

        // Radio Toggle
        const rbs = document.getElementsByName("chat_mode");
        for (const rb of rbs) {
            rb.addEventListener("change", (e) => this.toggleSettingsGroups(e.target.value));
        }

        // Clear History
        document.getElementById("clear-history-btn").addEventListener("click", () => {
            if (confirm("¿Estás seguro de borrar todo el historial?")) {
                this.state.history = [];
                this.saveSettings();
                this.renderHistory();
                this.elements.modal.style.display = "none";
            }
        });

        // Tests
        const testApiBtn = document.getElementById("test-api-connection");
        if (testApiBtn) testApiBtn.addEventListener("click", () => this.runTest("api"));

        const testModelBtn = document.getElementById("test-model-connection");
        if (testModelBtn) testModelBtn.addEventListener("click", () => this.runTest("model"));
    }

    async runTest(type) {
        const feedback = document.getElementById("config-feedback");
        feedback.innerText = "Probando...";
        feedback.style.color = "#58a6ff";

        try {
            if (type === "api") {
                const p = document.getElementById("ai-provider-select").value;
                const k = document.getElementById("ai-api-key").value;
                await this.apiAI.testConnection({ provider: p, apiKey: k });
            } else {
                const u = document.getElementById("ai-model-url").value;
                await this.apiAI.testConnection({ provider: "custom", modelUrl: u });
            }
            feedback.innerText = "✅ Conexión Exitosa";
            feedback.style.color = "#2ea043";
        } catch (e) {
            feedback.innerText = "❌ Error: " + e.message;
            feedback.style.color = "#ff7b72";
        }
    }

    toggleSettingsGroups(mode) {
        document.getElementById("api-config-group").style.display = mode === "api" ? "block" : "none";
        document.getElementById("local-config-group").style.display = mode === "local" ? "block" : "none";
        document.getElementById("model-config-group").style.display = mode === "model" ? "block" : "none";
    }
}
