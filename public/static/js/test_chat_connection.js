/**
 * Test Chat Connection
 * Run this in the browser console to verify your API Key or Model URL.
 */

async function testConnection() {
    const apiKey = localStorage.getItem('python_tutor_chat_api_key');
    const modelUrl = localStorage.getItem('python_tutor_model_url');
    const mode = localStorage.getItem('python_tutor_chat_mode');

    console.log(`🔍 Testing Connection (Mode: ${mode})...`);

    if (mode === 'api') {
        if (!apiKey) {
            console.error("❌ No API Key found in localStorage.");
            return;
        }
        console.log("🔑 API Key found.");
        // Note: This is a generic test. Actual endpoint depends on provider.
        console.log("⚠️  To test fully, use the 'Probar Conexión' button in the UI.");

    } else if (mode === 'model') {
        if (!modelUrl) {
            console.error("❌ No Model URL found.");
            return;
        }
        console.log(`🌐 Testing URL: ${modelUrl}`);
        try {
            const resp = await fetch(modelUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: [{ role: 'user', content: 'ping' }] })
            });
            if (resp.ok) console.log("✅ Connection Successful!");
            else console.error(`❌ Server returned ${resp.status}: ${resp.statusText}`);
        } catch (e) {
            console.error("❌ Connection Failed:", e.message);
        }
    } else {
        console.log("ℹ️  Local mode selected. Check WebLLM status in UI.");
    }
}

// Auto-run if loaded directly
// testConnection();
