/**
 * ai_cpu.js
 * Handles Lite AI execution using CPU (WASM) via transformers.js.
 * Universal fallback mode.
 */

import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.16.0';

env.allowLocalModels = false;
env.useBrowserCache = true;

export class CpuAI {
    constructor() {
        this.generator = null;
        this.modelId = "Xenova/Qwen1.5-0.5B-Chat";
        this.isLoaded = false;
        this.isLoading = false;
        this.device = 'wasm'; // Force CPU
    }

    async init(progressCallback) {
        if (this.isLoaded) return true;
        this.isLoading = true;

        try {
            this.generator = await pipeline('text-generation', this.modelId, {
                device: this.device,
                dtype: 'q8', // 8-bit quantization for CPU stability
                progress_callback: (data) => {
                    if (data.status === 'progress' && progressCallback) {
                        progressCallback(`Descargando (Lite) ${data.file}`, data.progress / 100);
                    }
                }
            });

            this.isLoaded = true;
            this.isLoading = false;
            return true;

        } catch (error) {
            console.error("Lite AI (CPU) Init Error:", error);
            this.isLoading = false;
            throw error;
        }
    }

    async sendMessageCpuModel(messages, onChunk) {
        if (!this.isLoaded) throw new Error("Lite AI is not loaded.");

        try {
            const prompt = messages.map(m => `<|im_start|>${m.role}\n${m.content}<|im_end|>`).join("\n") + "\n<|im_start|>assistant\n";

            const output = await this.generator(prompt, {
                max_new_tokens: 256, // Shorter generation for CPU
                temperature: 0.7,
                do_sample: true,
                return_full_text: false,
            });

            const reply = output[0].generated_text;

            if (onChunk) {
                const words = reply.split(" ");
                for (const word of words) {
                    onChunk(word + " ");
                    await new Promise(r => setTimeout(r, 50)); // Slower typing
                }
            }

            return reply;

        } catch (error) {
            console.error("Lite AI Generation Error:", error);
            throw error;
        }
    }
}
