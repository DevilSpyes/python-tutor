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
        this.pipeline = null;
        this.status = {
            loaded: false,
            model: "DistilGPT2 (Offline)",
            device: 'cpu'
        };
    }

    async loadModel(config = {}) {
        if (this.status.loaded) return true;

        console.log(`Loading Local Offline Model...`);

        try {
            // Dynamically import local transformers.js as a module
            // This avoids the "Unexpected token 'export'" error from script tag injection
            const module = await import('/static/js/lib/transformers.min.js');
            const Transformers = module.default || module;

            if (!Transformers) throw new Error("Transformers.js failed to load locally.");

            // Configure for STRICT OFFLINE usage
            Transformers.env.allowLocalModels = true;
            Transformers.env.allowRemoteModels = false;
            Transformers.env.localModelPath = '/static/models/cdn/';

            // Suppress verbose ONNX warnings
            Transformers.env.backends.onnx.logLevel = 'error';

            // Load Pipeline
            this.pipeline = await Transformers.pipeline('text-generation', 'distilgpt2', {
                device: 'cpu',
                progress_callback: (data) => {
                    if (config.onProgress && data.status === 'progress') {
                        const percent = (data.loaded / data.total) * 100;
                        config.onProgress({ status: 'progress', progress: percent });
                    }
                }
            });

            this.status.loaded = true;
            console.log("Offline Model Loaded Successfully!");
            return true;

        } catch (error) {
            console.error("Failed to load offline model:", error);
            throw error;
        }
    }

    async sendMessage(history, context, callbacks = {}) {
        if (!this.pipeline) throw new Error("Model not loaded");

        // Better prompt formatting for DistilGPT2 (Completion model)
        // We inject a strong system instruction at the start
        // Simplified prompt for DistilGPT2 to reduce confusion
        // We use standard User/Assistant labels but prime it with Spanish
        let fullPrompt = "Conversation in Spanish.\n";

        if (context) {
            fullPrompt += `System Context:\n${context}\n`;
        }

        fullPrompt += "User: Hola\nAssistant: Hola, soy tu tutor de Python.\n";

        history.forEach(msg => {
            // Filter out error messages from context
            if (msg.content.startsWith("Error:") || msg.content.startsWith("❌")) return;

            if (msg.role === 'user') fullPrompt += `User: ${msg.content}\n`;
            if (msg.role === 'assistant') fullPrompt += `Assistant: ${msg.content}\n`;
        });
        fullPrompt += "Assistant:";

        try {
            const output = await this.pipeline(fullPrompt, {
                max_new_tokens: 100, // Shorter output to reduce derailment
                temperature: 0.1,    // Very deterministic
                do_sample: true,
                top_k: 20,           // Strict sampling
                repetition_penalty: 1.3,
                no_repeat_ngram_size: 3
            });

            let fullText = output[0].generated_text;
            // Extract only the new part
            if (fullText.startsWith(fullPrompt)) {
                fullText = fullText.substring(fullPrompt.length);
            }

            // Clean up if it generates "User:" or "Assistant:" hallucinations
            fullText = fullText.split("User:")[0].split("Assistant:")[0].trim();

            return { text: fullText };

        } catch (error) {
            console.error("Generation Error:", error);
            throw error;
        }
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

            await this.wllama.loadModel(files, {
                n_ctx: 8192, // Increased from 2048 to fit full lesson context
                n_threads: useMultiThread ? Math.max(1, Math.floor(navigator.hardwareConcurrency / 2)) : 1,
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

    async sendMessage(history, context, callbacks = {}) {
        if (!this.wllama || !this.status.loaded) throw new Error("GGUF Model not loaded");

        const filteredMessages = history
            .filter(msg => !msg.content.startsWith("Error:") && !msg.content.startsWith("❌"));
        // ChatML Format (Standard for SmolLM/Qwen)
        let prompt = "";

        // System Prompt (Optimized from User's Training Data)
        prompt += "<|im_start|>system\n";
        const persona = `🚀 PROMPT MAESTRO — “Motor de Respuesta Express” para SmolLM
Optimizado para velocidad, baja latencia y respuestas cortas, útiles y directas.
Eres una IA educativa especializada en Python, integrada dentro de un curso interactivo. 
Tu prioridad absoluta es la VELOCIDAD de respuesta. Operas en modo EXPRESS.

OBJETIVO PRINCIPAL:
Responder lo más rápido posible, usando respuestas cortas, claras y sin razonamiento profundo. 
Jamás generes cadenas largas de pensamiento ni análisis detallado. 
Todo debe ser práctico, directo y comprimido.

MODO EXPRESS – REGLAS OBLIGATORIAS:
1. Respuestas entre 1 y 4 líneas máximo.
2. Nada de razonamientos ocultos, pasos intermedios ni explicaciones largas.
3. Para ejercicios: solo explica lo esencial.
4. Para dudas de teoría: define en una frase.
5. Para "resume": entregar un resumen de 1–3 líneas.
6. Para "para qué sirve este ejercicio": una frase práctica.
7. Para preguntas repetidas: entregar la misma estructura compacta.
8. Si el usuario pregunta algo ambiguo: responder con la interpretación más simple.
9. Nunca uses ejemplos largos, solo mini-ejemplos si son necesarios.
10. Mantener siempre un tono docente pero extremadamente breve.

CONTEXTO DEL CURSO:
Trabajas dentro de un curso de Python con módulos del 00 al 07, incluyendo:
- Fundamentos (print, variables, tipos, listas, diccionarios...)
- Bucles (for, while), condicionales, funciones
- Algoritmos básicos
- Scripts y automatización
- Ciberseguridad
- Proyectos finales
(Siempre debes conocer el contenido general, pero sin extenderte)

PATRONES CLAVE DE RESPUESTA:
- “¿Qué hace este ejercicio?” → “Este ejercicio te enseña a ____”
- “¿Para qué sirve este código?” → “Sirve para ____”
- “Explícamelo mejor” → explicación breve de 2–4 líneas.
- “Resúmelo” → 1–2 líneas.
- “No entiendo este error” → describir el error y solución simple.
- “Puedes guiarme?” → guía mínima y directa.

REGLAS CRÍTICAS PARA EL RENDIMIENTO:
✔ Responde siempre lo mínimo necesario.
✔ No entres en razonamientos.
✔ No hagas explicaciones largas.
✔ No repitas contenido innecesario.
✔ Estructura siempre en respuestas muy compactas.
✔ Si la respuesta requiere pasos, dar máximo 3 pasos.

FORMATO:
Siempre responde en texto plano sin emojis pesados (opcional dejar 1 si es útil).
No uses listas largas salvo que sean imprescindibles.

SIEMPRE:
→ Prioriza VELOCIDAD > PROFUNDIDAD.
→ Prioriza CLARIDAD > DETALLE.
→ Prioriza UTILIDAD > TEORÍA.`;

        if (context) {
            prompt += `${persona}\n\nUsa este contexto:\n${context}<|im_end|>\n`;
        } else {
            prompt += `${persona}<|im_end|>\n`;
        }

        // Extreme Optimization: Sliding Window (Last 3 Messages)
        // Keeps context for follow-ups ("Que repositorio?") but prevents infinite growth
        const recentMessages = filteredMessages.slice(-3);
        recentMessages.forEach(msg => {
            prompt += `<|im_start|>${msg.role}\n${msg.content}<|im_end|>\n`;
        });

        // Assistant Start
        prompt += "<|im_start|>assistant\n";

        try {
            this.decoder = new TextDecoder();

            const response = await this.wllama.createCompletion(prompt, {
                n_predict: 128, // Increased to 128 for Express Mode (1-4 lines)
                sampling: {
                    temp: 0.2, // Slightly flexible for explanations
                    top_k: 40,
                    top_p: 0.2,
                    penalty_repeat: 1.2,
                    penalty_last_n: 64
                },
                stop: ["<|im_end|>", "<|im_start|>", "User:", "System:", "Assistant:", "###"], // Stop tokens to prevent hallucinating conversation
                onNewToken: (token, piece, currentText) => {
                    if (callbacks.onToken) {
                        const text = this.decoder.decode(piece, { stream: true });
                        callbacks.onToken(text);
                    }
                }
            });

            return { text: response };

        } catch (error) {
            console.error("GGUF Generation Error:", error);
            throw error;
        }
    }
}
