/**
 * ai_local.js
 * Handles Local AI execution using WebGPU via transformers.js.
 * High performance mode.
 */

import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.16.0';

// Configuration
env.allowLocalModels = false; // Allow fetching from HF Hub
env.useBrowserCache = true;
// env.backends.onnx.wasm.numThreads = 1; // Not needed for WebGPU

export class LocalAI {
    constructor() {
        this.generator = null;
        this.modelId = "Xenova/Qwen1.5-0.5B-Chat";
        this.isLoaded = false;
        this.isLoading = false;
        this.device = 'webgpu';
    }

    async checkWebGPUSupport() {
        if (!navigator.gpu) return false;
        try {
            const adapter = await navigator.gpu.requestAdapter();
            return !!adapter;
        } catch (e) {
            return false;
        }
    }

    async init(progressCallback) {
        if (this.isLoaded) return true;
        this.isLoading = true;

        try {
            this.generator = await pipeline('text-generation', this.modelId, {
                device: this.device,
                dtype: 'q4', // Quantized for speed/memory
                progress_callback: (data) => {
                    if (data.status === 'progress' && progressCallback) {
                        progressCallback(`Descargando (GPU) ${data.file}`, data.progress / 100);
                    } else if (data.status === 'ready') {
                        if (progressCallback) progressCallback("Modelo listo", 1);
                    }
                }
            });

            this.isLoaded = true;
            this.isLoading = false;
            return true;

        } catch (error) {
            console.error("Local AI (WebGPU) Init Error:", error);
            this.isLoading = false;
            throw error;
        }
    }

    async sendMessageLocalModel(messages, onChunk) {
        if (!this.isLoaded) throw new Error("Local AI is not loaded.");

        try {
            // Simple chat template construction
            const prompt = messages.map(m => `<|im_start|>${m.role}\n${m.content}<|im_end|>`).join("\n") + "\n<|im_start|>assistant\n";

            const output = await this.generator(prompt, {
                max_new_tokens: 512,
                temperature: 0.7,
                do_sample: true,
                top_k: 50,
                return_full_text: false,
                callback_function: (beams) => {
                    const decodedText = this.generator.tokenizer.decode(beams[0].output_token_ids, { skip_special_tokens: true });
                    // Streaming logic: This is a simplification. 
                    // Real streaming with transformers.js requires tracking previous length.
                }
            });

            const reply = output[0].generated_text;

            // Simulate streaming for UI consistency since true streaming is complex to implement perfectly in one go
            if (onChunk) {
                const words = reply.split(" ");
                for (const word of words) {
                    onChunk(word + " ");
                    await new Promise(r => setTimeout(r, 10));
                }
            }

            return reply;

        } catch (error) {
            console.error("Local AI Generation Error:", error);
            throw error;
        }
    }
}
