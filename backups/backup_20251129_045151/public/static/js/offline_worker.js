// offline_worker.js
// Runs Transformers.js in a Web Worker to prevent UI freeze

let generator = null;
let Transformers = null;

self.addEventListener('message', async (event) => {
    const { type, data } = event.data;

    try {
        if (type === 'load') {
            await loadModel(data);
        } else if (type === 'generate') {
            await generateText(data);
        }
    } catch (error) {
        self.postMessage({ status: 'error', error: error.message || String(error) });
    }
});

async function loadModel(config) {
    self.postMessage({ status: 'loading', message: 'Iniciando Worker...' });

    try {
        // Dynamic Import (Local)
        const module = await import('/static/js/transformers.min.js');
        Transformers = module.default || module;
        const { pipeline, env } = Transformers;

        // Configure environment
        env.allowLocalModels = false;
        env.allowRemoteModels = true;

        // Point WASM to CDN to ensure it loads (since we only downloaded the JS)
        env.backends.onnx.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/';

        // Optimize threads based on config
        if (config.threads) {
            env.backends.onnx.wasm.numThreads = config.threads;
        }

        self.postMessage({ status: 'progress', progress: 10, message: 'Cargando motor Qwen 2.5...' });

        // Qwen 2.5 0.5B Instruct (ONNX)
        generator = await pipeline('text-generation', 'onnx-community/Qwen2.5-0.5B-Instruct', {
            dtype: 'q8', // Use 8-bit quantization for CPU stability (WASM)
            device: 'webgpu', // Try WebGPU first, fallback to cpu? No, let's stick to 'cpu' for safety or let it auto-detect if we want. 
            // The user has 'cpu' in the original code. Let's stick to 'cpu' for broad compatibility as requested "similar consumption".
            // WebGPU is faster but might not be available.
            device: 'wasm',
            progress_callback: (progressData) => {
                if (progressData.status === 'progress') {
                    // Map 0-100 of download to 10-90 of total load
                    const p = 10 + (progressData.loaded / progressData.total) * 80;
                    self.postMessage({ status: 'progress', progress: p, message: 'Descargando modelo...' });
                }
            }
        });

        self.postMessage({ status: 'ready', message: 'Modelo cargado.' });

    } catch (e) {
        throw new Error(`Fallo al importar Transformers.js: ${e.message}`);
    }
}

async function generateText(params) {
    if (!generator) throw new Error("Modelo no cargado.");

    const { prompt, max_new_tokens, temperature } = params;

    // Polyfill TextStreamer if missing (for older transformers.js versions)
    let StreamerClass = Transformers.TextStreamer;

    if (!StreamerClass) {
        console.warn("TextStreamer not found, using custom polyfill.");
        StreamerClass = class CustomStreamer {
            constructor(tokenizer, { callback_function, skip_special_tokens }) {
                this.tokenizer = tokenizer;
                this.callback = callback_function;
                this.skip_special_tokens = skip_special_tokens;
                this.tokens = [];
            }

            put(token_ids) {
                // token_ids is a Tensor or array. We need to handle it.
                // For simplicity in older versions, it might be just an array of IDs.
                // We'll try to decode the *new* tokens.

                // Note: This is a simplified implementation. 
                // Proper streaming requires tracking previous tokens to handle partial unicode.
                // For now, let's just decode everything and send the diff? 
                // Or just send the whole text and let UI handle it?
                // The UI appends, so we need chunks.

                // Actually, let's just try to decode the last token.
                const value = token_ids[0]; // Assuming batch size 1
                // If it's a Tensor, get data.
                const id = value.data ? value.data[0] : value;

                const text = this.tokenizer.decode([id], { skip_special_tokens: this.skip_special_tokens });
                if (this.callback) this.callback(text);
            }

            end() { }
        };
    }

    // Custom Streamer to send tokens back to main thread
    const streamer = new StreamerClass(generator.tokenizer, {
        skip_prompt: true,
        skip_special_tokens: true,
        callback_function: (text) => {
            self.postMessage({ status: 'token', token: text });
        }
    });

    const output = await generator(prompt, {
        max_new_tokens: max_new_tokens || 256,
        temperature: temperature || 0.4,
        do_sample: true,
        top_k: params.top_k || 40,
        top_p: params.top_p || 0.9,
        repetition_penalty: params.repetition_penalty || 1.2,
        streamer: streamer,
        return_full_text: false
    });

    // Send final result
    let fullText = output[0].generated_text;
    fullText = fullText.replace("<|im_end|>", "").trim();

    self.postMessage({ status: 'complete', text: fullText });
}

