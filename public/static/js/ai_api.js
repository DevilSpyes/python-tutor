/**
 * ai_api.js
 * Handles communication with external AI APIs (OpenAI, Groq, Custom).
 */

export class ApiAI {
    constructor() {
        this.endpoints = {
            openai: "https://api.openai.com/v1/chat/completions",
            groq: "https://api.groq.com/openai/v1/chat/completions",
            deepseek: "https://api.deepseek.com/v1/chat/completions"
        };

        this.models = {
            openai: "gpt-4o",
            groq: "llama3-8b-8192",
            deepseek: "deepseek-chat"
        };
    }

    /**
     * Sends a message to an external API.
     * @param {Array} messages - History of messages.
     * @param {Object} config - { provider, apiKey, model, modelUrl }.
     * @param {function} onChunk - Callback for streaming (simulated for now if fetch doesn't support stream easily).
     */
    async sendMessageAPIModel(messages, config, onChunk) {
        const { provider, apiKey, model, modelUrl } = config;

        let endpoint = this.endpoints[provider];
        let modelName = model || this.models[provider];

        // Custom Model Mode
        if (provider === 'custom') {
            if (!modelUrl) throw new Error("Missing Model URL for custom provider.");
            endpoint = modelUrl;
            // Custom models might not need a specific model name, but we send one just in case
            modelName = model || "custom-model";
        } else {
            if (!apiKey) throw new Error(`Missing API Key for ${provider}.`);
        }

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": apiKey ? `Bearer ${apiKey}` : undefined
                },
                body: JSON.stringify({
                    model: modelName,
                    messages: messages,
                    stream: false // For simplicity in this version, we'll do non-streaming first. Streaming can be added if needed.
                })
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(`API Error ${response.status}: ${errData.error?.message || response.statusText}`);
            }

            const data = await response.json();
            const reply = data.choices?.[0]?.message?.content || data.response || "No response content.";

            // Simulate streaming for UI consistency
            if (onChunk) {
                // Split by words to simulate typing
                const words = reply.split(" ");
                for (const word of words) {
                    onChunk(word + " ");
                    await new Promise(r => setTimeout(r, 20)); // Tiny delay
                }
            }

            return reply;

        } catch (error) {
            console.error("API Request Error:", error);
            throw error;
        }
    }

    async testConnection(config) {
        try {
            await this.sendMessageAPIModel(
                [{ role: "user", content: "ping" }],
                config,
                null
            );
            return true;
        } catch (e) {
            throw e;
        }
    }
}
