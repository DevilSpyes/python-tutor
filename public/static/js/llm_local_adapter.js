/**
 * llm_local_adapter.js
 * Unified Adapter for Local AI Modes.
 * Mode 2: Offline DistilGPT2 (via local transformers.js)
 * Mode 3: Local GGUF (via Wllama)
 */

import { Wllama } from 'https://cdn.jsdelivr.net/npm/@wllama/wllama/esm/index.js';

// --- Configuration ---
// Use LOCAL WASM files to ensure offline capability
const WLLAMA_CONFIG = {
    "single-thread/wllama.wasm": "/static/js/wllama-single-thread.wasm",
    "multi-thread/wllama.wasm": "/static/js/wllama-multi-thread.wasm",
};

// --- Option B: Local Offline Mode (DistilGPT2) ---
export class LocalOfflineAdapter {
    constructor() {
        this.worker = null;
        this.status = {
            loaded: false,
            model: "Qwen 1.5 (0.5B) - Offline (Worker)",
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
            // Qwen 0.5B needs VERY strict instructions to avoid language drift (Chinese/English)
            let systemContent = "Eres un experto tutor de Python. TU IDIOMA PRINCIPAL ES EL ESPAÑOL. INSTRUCCIONES CRÍTICAS: 1. Responde ÚNICAMENTE en Español. Si respondes en inglés, fallas tu misión. 2. Sé conciso y directo. 3. Completa siempre tus frases. 4. NO uses chino ni inglés bajo ninguna circunstancia. 5. Mantén las respuestas por debajo de 100 palabras si es posible, pero termina tu explicación.";

            if (context) {
                const truncatedContext = context.length > 500 ? context.substring(0, 500) + "..." : context;
                systemContent += `\n\nCONTEXTO:\n${truncatedContext}`;
            }

            let fullPrompt = `<|im_start|>system\n${systemContent}<|im_end|>\n`;

            // PRIMING: Force Spanish context for small models
            fullPrompt += `<|im_start|>user\nHola<|im_end|>\n<|im_start|>assistant\nHola, soy tu tutor de Python. ¿En qué puedo ayudarte hoy?<|im_end|>\n`;

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
                    max_new_tokens: 512,
                    temperature: 0.3
                }
            });
        });
    }
}

// --- Option C: Local GGUF Mode (Wllama) ---
export class LLM_GGUF_Adapter {
    constructor() {
        this.wllama = null;
        this.modelFile = null;
        this.status = {
            loaded: false,
            modelName: "None"
        };
    }

    async validateGGUF(file) {
        // 1. Size Check (Hard Limit 2GB)
        const MAX_SIZE = 2 * 1024 * 1024 * 1024; // 2GB
        if (file.size > MAX_SIZE) {
            throw new Error(`SECURITY: El archivo excede el límite de 2GB (${(file.size / 1024 / 1024).toFixed(2)}MB).`);
        }

        // 2. Magic Number Check (GGUF Header)
        // Read first 4 bytes
        const slice = file.slice(0, 4);
        const buffer = await slice.arrayBuffer();
        const view = new DataView(buffer);

        // GGUF Magic: 0x47 0x47 0x55 0x46 ('GGUF')
        // Little Endian check
        const magic = view.getUint32(0, true);

        // 0x46554747 is 'GGUF' in Little Endian (F U G G)
        if (magic !== 0x46554747) {
            throw new Error("SECURITY: Archivo inválido. No se detectó la firma 'GGUF'.");
        }

        return true;
    }

    async loadModel(input, callbacks = {}) {
        if (!input) throw new Error("No GGUF file or URL provided");

        // Handle URL
        if (typeof input === 'string' && input.startsWith('http')) {
            return this.loadFromUrl(input, callbacks);
        }

        const files = Array.isArray(input) ? input : [input];
        this.modelFile = files[0];
        this.status.modelName = this.modelFile.name;

        console.log(`Initializing Wllama for GGUF: ${this.modelFile.name}...`);

        try {
            this.wllama = new Wllama(WLLAMA_CONFIG);

            // Check for SharedArrayBuffer support (required for multi-threading)
            const useMultiThread = window.crossOriginIsolated && navigator.hardwareConcurrency > 1;

            // OPTIMIZATION: Limit threads to prevent UI freeze
            // Use half of available cores, but max 4. Minimum 1.
            const safeThreads = useMultiThread
                ? Math.max(1, Math.min(4, Math.floor(navigator.hardwareConcurrency / 2)))
                : 1;

            console.log(`Wllama Config: Threads=${safeThreads}, MultiThread=${useMultiThread}`);

            await this.wllama.loadModel(files, {
                n_ctx: 2048, // Reduced to 2048 for better compatibility
                n_threads: safeThreads,
                progressCallback: (data) => {
                    if (callbacks.onProgress) {
                        const percent = (data.loaded / data.total) * 100;
                        callbacks.onProgress({ status: 'progress', progress: percent });
                    }
                }
            });

            this.status.loaded = true;
            console.log("GGUF Model Loaded Successfully!");
            return true;

        } catch (error) {
            console.error("Failed to load GGUF model:", error);
            throw error;
        }
    }

    async loadFromUrl(url, callbacks = {}) {
        console.log(`Downloading GGUF from: ${url}`);
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to download: ${response.statusText}`);

            const contentLength = response.headers.get('content-length');
            const total = parseInt(contentLength, 10);
            let loaded = 0;

            const reader = response.body.getReader();
            const chunks = [];

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                chunks.push(value);
                loaded += value.length;
                if (callbacks.onProgress && total) {
                    callbacks.onProgress({ status: 'downloading', progress: (loaded / total) * 100 });
                }
            }

            const blob = new Blob(chunks);
            // Create a fake File object to satisfy Wllama's expectation or just pass Blob
            const file = new File([blob], "downloaded_model.gguf");

            // Pass to normal load logic
            return this.loadModel(file, callbacks);

        } catch (error) {
            console.error("Download Error:", error);
            throw error;
        }
    }

    applyTemplate(history, context, template = 'chatml') {
        let fullPrompt = "";
        const systemMsg = "Eres un asistente experto en Python. TU IDIOMA ES EL ESPAÑOL. Responde ÚNICAMENTE en español. Si el usuario te habla en otro idioma, responde en español. NO uses inglés bajo ninguna circunstancia. Sé conciso (máx 150 palabras) pero completo. NO dejes frases a medias.";

        let systemContent = systemMsg;
        if (context) {
            const truncatedContext = context.length > 600 ? context.substring(0, 600) + "..." : context;
            systemContent += `\n\nCONTEXTO:\n${truncatedContext}`;
        }

        const recentHistory = history.slice(-3).filter(msg => !msg.content.startsWith("Error:") && !msg.content.startsWith("❌"));

        switch (template) {
            case 'llama3':
                // Llama 3 Format
                fullPrompt += `<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n${systemContent}<|eot_id|>`;
                recentHistory.forEach(msg => {
                    fullPrompt += `<|start_header_id|>${msg.role}<|end_header_id|>\n\n${msg.content}<|eot_id|>`;
                });
                fullPrompt += `<|start_header_id|>assistant<|end_header_id|>\n\n`;
                break;

            case 'alpaca':
                // Alpaca Format
                fullPrompt += `### Instruction:\n${systemContent}\n\n`;
                recentHistory.forEach(msg => {
                    if (msg.role === 'user') fullPrompt += `### Input:\n${msg.content}\n\n`;
                    if (msg.role === 'assistant') fullPrompt += `### Response:\n${msg.content}\n\n`;
                });
                fullPrompt += `### Response:\n`;
                break;

            case 'mistral':
                // Mistral Format (approximate)
                fullPrompt += `<s>[INST] ${systemContent} [/INST] Entendido.</s>`;
                recentHistory.forEach(msg => {
                    if (msg.role === 'user') fullPrompt += `[INST] ${msg.content} [/INST]`;
                    if (msg.role === 'assistant') fullPrompt += `${msg.content}</s>`;
                });
                break;

            case 'gemma':
                // Gemma Format
                fullPrompt += `<start_of_turn>user\n${systemContent}\n`;
                recentHistory.forEach(msg => {
                    fullPrompt += `<start_of_turn>${msg.role === 'assistant' ? 'model' : 'user'}\n${msg.content}<end_of_turn>\n`;
                });
                fullPrompt += `<start_of_turn>model\n`;
                break;

            case 'qa':
                // Q&A Format (Best for Base Models)
                fullPrompt += `${systemContent}\n\n`;
                recentHistory.forEach(msg => {
                    if (msg.role === 'user') fullPrompt += `Q: ${msg.content}\n`;
                    if (msg.role === 'assistant') fullPrompt += `A: ${msg.content}\n`;
                });
                fullPrompt += `A:`;
                break;

            case 'raw':
                // Raw Format
                fullPrompt += `${systemContent}\n\n`;
                recentHistory.forEach(msg => {
                    fullPrompt += `${msg.role.toUpperCase()}: ${msg.content}\n`;
                });
                fullPrompt += `ASSISTANT:`;
                break;

            case 'chatml':
            default:
                // ChatML Format (Default)
                fullPrompt += `<|im_start|>system\n${systemContent}<|im_end|>\n`;
                recentHistory.forEach(msg => {
                    fullPrompt += `<|im_start|>${msg.role}\n${msg.content}<|im_end|>\n`;
                });
                fullPrompt += "<|im_start|>assistant\n";
                break;
        }

        return fullPrompt;
    }

    async sendMessage(history, context, callbacks = {}, config = {}) {
        if (!this.wllama || !this.status.loaded) throw new Error("GGUF Model not loaded");

        const template = config.template || 'chatml';
        const fullPrompt = this.applyTemplate(history, context, template);

        try {
            this.decoder = new TextDecoder();

            // Support for AbortSignal
            const signal = config.signal;

            const completionPromise = this.wllama.createCompletion(fullPrompt, {
                n_predict: 1024,
                sampling: {
                    temp: 0.2,
                    top_k: 40,
                    top_p: 0.9,
                    penalty_repeat: 1.1,
                    penalty_last_n: 64
                },
                // Stop tokens for various formats
                stop: ["<|im_end|>", "<|im_start|>", "<|eot_id|>", "</s>", "<end_of_turn>", "###", "[/urls]"],
                onNewToken: (token, piece, currentText) => {
                    if (signal && signal.aborted) return; // Stop callback if aborted
                    if (callbacks.onToken) {
                        const text = this.decoder.decode(piece, { stream: true });
                        callbacks.onToken(text);
                    }
                },
                signal: signal // Pass signal to Wllama
            });

            // 240s Timeout Race (Increased for mobile stability with 4k context)
            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error("Timeout: La IA tardó demasiado en responder (posible falta de memoria).")), 240000)
            );

            const response = await Promise.race([completionPromise, timeoutPromise]);

            return { text: response };

        } catch (error) {
            console.error("GGUF Generation Error:", error);

            // Auto-Recovery for Context Cache Error
            if (error.message.includes("context cache") || error.message.includes("n_ctx")) {
                console.warn("Context Cache Full. Resetting Wllama instance...");
                if (this.wllama) {
                    await this.wllama.exit(); // Kill worker
                    this.wllama = null;
                }
                this.status.loaded = false;
                throw new Error("⚠️ Memoria llena. Reiniciando motor IA... Por favor, intenta de nuevo en 5 segundos.");
            } else if (error.message.includes("abort signal")) {
                throw new Error("⚠️ Error de Memoria (Abort). El modelo es demasiado grande o el contexto muy largo para tu dispositivo. Intenta usar un modelo más pequeño (ej. Qwen 0.5B) o recargar la página.");
            }

            throw error;
        }
    }
}
