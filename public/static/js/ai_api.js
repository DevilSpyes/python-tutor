/**
 * ai_api.js
 * Handles communication with external AI APIs (OpenAI, Groq, Custom).
 */

export class ApiAI {
    constructor() {
        this.endpoints = {
            openai: "https://api.openai.com/v1/chat/completions",
            groq: "https://api.groq.com/openai/v1/chat/completions",
            deepseek: "https://api.deepseek.com/chat/completions"
        };

        this.models = {
            openai: "gpt-4o",
            groq: "llama-3.3-70b-versatile",
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
            if (!modelUrl) throw new Error("Missing Base URL for custom provider.");
            endpoint = modelUrl;
            // Ensure endpoint ends with /chat/completions if not present (heuristic)
            if (!endpoint.endsWith('/chat/completions') && !endpoint.endsWith('/generate')) {
                // Common convention, but let's trust the user input mostly. 
                // Actually, let's just use what they gave.
            }
            modelName = model || "custom-model";
        } else {
            if (!apiKey) throw new Error(`Missing API Key for ${provider}.`);
        }

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": apiKey ? `Bearer ${apiKey.trim().replace(/[^\x00-\x7F]/g, "")}` : undefined
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
                // Split by characters for smoother typing and to preserve exact whitespace
                const chars = reply.split("");
                for (const char of chars) {
                    onChunk(char);
                    // Dynamic delay: faster for long text, slower for short
                    const delay = reply.length > 500 ? 2 : 10;
                    await new Promise(r => setTimeout(r, delay));
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
