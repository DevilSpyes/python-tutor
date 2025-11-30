
// Mock Browser Globals
global.fetch = async (url) => {
    console.log(`[MockFetch] Fetching: ${url}`);
    if (url.includes('knowledge_base_lite.json')) return { ok: true, json: async () => ({}) };
    if (url.includes('exercises_v2.json')) return { ok: true, json: async () => ([]) };
    if (url.includes('glossary.json')) return { ok: true, json: async () => ({}) };
    return { ok: false, status: 404 };
};

// Mock DOM if needed (minimal)
global.document = {
    getElementById: () => null,
    querySelector: () => null
};

// Import the Adapter (we need to read the file content and eval it, or require it if it was a module)
// Since it's a frontend file, I'll read it and wrap it.
const fs = require('fs');
const path = require('path');

const adapterPath = '/home/devilspy/.gemini/antigravity/scratch/python_tutor/public/static/js/llm_local_adapter.js';
const adapterCode = fs.readFileSync(adapterPath, 'utf8');

// Hack to load the class
const moduleExports = {};
const cleanCode = adapterCode.replace(/export class ProfessorLiteAdapter/, 'global.ProfessorLiteAdapter = class ProfessorLiteAdapter').replace(/export default/g, 'moduleExports.default =');
eval(cleanCode);
// const ProfessorLiteAdapter = global.ProfessorLiteAdapter; // No need, it's global now

async function runSimulation() {
    console.log("--- Starting Simulation ---");

    // 1. Instantiate
    const adapter = new ProfessorLiteAdapter();
    console.log("1. Instantiated Adapter");

    // 2. Load Model
    console.log("2. Loading Model...");
    try {
        await adapter.loadModel({}, { onProgress: (msg) => console.log(`[Progress] ${msg.message}`) });
        console.log("   Model Loaded Successfully");
    } catch (e) {
        console.error("   Model Load Failed:", e);
        return;
    }

    // 3. Prepare Context (The exact string we expect)
    const context = `
Current Exercise: Welcome
\n<<<MODULE_SUMMARY>>>Módulo 04: Automatización y Scripts. Aprenderás a crear scripts útiles.<<<END_MODULE_SUMMARY>>>\n
`;

    // 4. Send Message
    console.log("3. Sending Message: 'que se hace en el modulo 4'");
    const history = [{ role: 'user', content: 'que se hace en el modulo 4' }];

    try {
        const response = await adapter.sendMessage(history, context, {
            onToken: (t) => process.stdout.write(t)
        });
        console.log("\n\n4. Response Received:");
        console.log(response.text);
    } catch (e) {
        console.error("\n   SendMessage Failed:", e);
    }
    console.log("--- Simulation Complete ---");
}

runSimulation();
