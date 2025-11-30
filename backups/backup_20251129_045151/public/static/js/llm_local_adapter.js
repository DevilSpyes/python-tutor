/**
 * llm_local_adapter.js
 * Unified Adapter for Local AI Modes.
 * Mode 2: Offline DistilGPT2 (via local transformers.js)
 * Mode 3: Local GGUF (via Wllama)
 */



// --- Option B: Local Offline Mode (DistilGPT2) ---
export class LocalOfflineAdapter {
    constructor() {
        this.worker = null;
        this.status = {
            loaded: false,
            model: "Qwen 2.5 (0.5B) - Offline (Worker)",
            device: 'cpu'
        };
        this.callbacks = {};
    }

    async loadModel(config = {}) {
        if (this.status.loaded) return true;

        console.log(`Loading Local Offline Model (Worker)...`);

        return new Promise((resolve, reject) => {
            this.worker = new Worker('/static/js/offline_worker.js', { type: 'module' });

            this.worker.onmessage = (event) => {
                const { status, data, error, progress, message, token, text } = event.data;

                if (status === 'error') {
                    console.error("Worker Error:", error);
                    if (this.callbacks.onError) this.callbacks.onError(error);
                    // If we are waiting for load, reject
                    if (!this.status.loaded) reject(new Error(error));
                }
                else if (status === 'progress') {
                    if (config.onProgress) config.onProgress({ status: 'progress', progress: progress, message });
                }
                else if (status === 'ready') {
                    this.status.loaded = true;
                    console.log("Worker Model Loaded!");
                    resolve(true);
                }
                else if (status === 'token') {
                    if (this.callbacks.onToken) this.callbacks.onToken(token);
                }
                else if (status === 'complete') {
                    if (this.callbacks.onComplete) this.callbacks.onComplete(text);
                }
            };

            this.worker.onerror = (err) => {
                const msg = err.message || "Unknown Worker Error";
                const file = err.filename || "unknown file";
                const line = err.lineno || "?";
                console.error(`Worker System Error: ${msg} (${file}:${line})`, err);
                reject(new Error(`Worker Failed: ${msg}`));
            };

            // Start Load
            // Calculate safe threads
            const safeThreads = (window.crossOriginIsolated && navigator.hardwareConcurrency > 1)
                ? Math.max(1, Math.min(4, Math.floor(navigator.hardwareConcurrency / 2)))
                : 1;

            this.worker.postMessage({
                type: 'load',
                data: {
                    threads: safeThreads,
                    // We can try to use local path if we want, but CDN is safer for worker imports initially
                    // localPath: '/static/models/cdn/' 
                }
            });
        });
    }

    async sendMessage(history, context, callbacks = {}) {
        if (!this.worker || !this.status.loaded) throw new Error("Model not loaded");

        // Store callbacks for this generation session
        this.callbacks.onToken = callbacks.onToken;

        return new Promise((resolve, reject) => {
            this.callbacks.onComplete = (text) => {
                resolve({ text });
            };
            this.callbacks.onError = (err) => {
                reject(new Error(err));
            };

            // Prepare Prompt
            // Qwen 2.5 0.5B works best with simple, positive instructions.
            let systemContent = "Eres un asistente útil que enseña Python. Responde siempre en Español. Sé breve y claro.";

            if (context) {
                const truncatedContext = context.length > 300 ? context.substring(0, 300) + "..." : context;
                systemContent += `\nCONTEXTO:\n${truncatedContext}`;
            }

            let fullPrompt = `<|im_start|>system\n${systemContent}<|im_end|>\n`;

            // NO PRIMING: Let the model respond directly to the user to avoid context drift.

            const recentHistory = history.slice(-3);
            recentHistory.forEach(msg => {
                if (msg.content.startsWith("Error:") || msg.content.startsWith("❌")) return;
                fullPrompt += `<|im_start|>${msg.role}\n${msg.content}<|im_end|>\n`;
            });
            fullPrompt += "<|im_start|>assistant\n";

            // Send to Worker
            this.worker.postMessage({
                type: 'generate',
                data: {
                    prompt: fullPrompt,
                    max_new_tokens: 256,
                    temperature: 0.6,
                    top_k: 40,
                    top_p: 0.8,
                    repetition_penalty: 1.15
                }
            });
        });
    }
}


