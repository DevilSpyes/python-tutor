import { AIChat } from "./ai_chat.js";
import { TypingSimulator } from "./typingSimulator.js";
import { LeftPanel } from "./ui_leftpanel.js";
import { TTSManager } from "./tts_manager.js"; // New Import

// Global State
let pyodide = null;
let currentLesson = null;
let allModules = [];
let aiChat = null;
let typingSim = null;
let leftPanel = null;
let ttsManager = null; // New State
let isTyping = false;

// DOM Elements
let elements = {};

function setupDOMElements() {
    elements = {
        loader: document.getElementById("initial-loader"),
        appContainer: document.getElementById("app-container"),
        workspaceContainer: document.getElementById("workspace-container"),
        moduleList: document.getElementById("module-list"),
        editor: document.getElementById("code-editor"),
        runBtn: document.getElementById("run-code"),
        terminalBody: document.getElementById("terminal-body"),
        lessonContent: document.getElementById("lesson-content"),
        lessonTitle: document.getElementById("lesson-title"),
        chatInput: document.getElementById("chat-input"),
        sendChatBtn: document.getElementById("send-chat"),
        chatHistory: document.getElementById("chat-history"),
        aiStatus: document.getElementById("ai-status"),
        settingsBtn: document.getElementById("ai-settings-btn"), // Updated ID
        settingsModal: document.getElementById("settings-modal"),
        closeSettings: document.getElementById("close-settings"),
        saveSettings: document.getElementById("save-settings"),
        apiKeyInput: document.getElementById("api-key"),
        providerSelect: document.getElementById("ai-provider"),
        aiPanel: document.querySelector(".ai-window") // Updated selector
    };

    // Debugging: Check for missing critical elements
    if (!elements.loader) console.error("CRITICAL: #initial-loader not found!");
    if (!elements.appContainer) console.error("CRITICAL: #app-container not found!");
}

async function loadPyodide() {
    logToTerminal("Cargando motor Python...", "info");
    if (!window.loadPyodide) {
        throw new Error("Pyodide script not loaded");
    }
    const p = await window.loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
    });
    return p;
}

function installNetworkFirewall() {
    const WHITELIST = [
        "cdn.jsdelivr.net",
        "pypi.org",
        "files.pythonhosted.org",
        "huggingface.co",
        "api.openai.com",
        "api.groq.com",
        "api.deepseek.com",
        "localhost",
        "127.0.0.1",
        "python-tutor-es.netlify.app",
        "translate.google.com"
    ];

    const originalFetch = window.fetch;
    window.fetch = async function (input, init) {
        let url;
        if (typeof input === 'string') {
            url = input;
        } else if (input instanceof URL) {
            url = input.href;
        } else if (input instanceof Request) {
            url = input.url;
        }

        if (url) {
            try {
                const parsedUrl = new URL(url, window.location.origin);
                const hostname = parsedUrl.hostname;

                // Allow if hostname ends with any whitelisted domain (to cover subdomains)
                const isAllowed = WHITELIST.some(domain =>
                    hostname === domain || hostname.endsWith("." + domain)
                );

                // SECURITY: Internal Port Scanning Protection
                // Only allow localhost on specific AI ports (Ollama: 11434, LM Studio: 1234, Dev: 8000/8080/5000)
                if (hostname === "localhost" || hostname === "127.0.0.1") {
                    const port = parsedUrl.port || (parsedUrl.protocol === 'https:' ? '443' : '80');
                    const ALLOWED_PORTS = ['11434', '1234', '5000', '8000', '8080'];
                    if (!ALLOWED_PORTS.includes(port)) {
                        console.error(`🔥 FIREWALL BLOCKED LOCAL PORT: ${port}`);
                        throw new Error(`SECURITY: Acceso a puerto local ${port} bloqueado. Solo se permiten puertos de IA (11434, 1234).`);
                    }
                }

                if (!isAllowed) {
                    console.error(`🔥 FIREWALL BLOCKED: ${url}`);
                    throw new Error(`SECURITY: Conexión bloqueada a ${hostname}. Solo se permiten dominios de confianza.`);
                }
            } catch (e) {
                if (e.message.startsWith("SECURITY")) throw e;
            }
        }
        return originalFetch.apply(this, arguments);
    };

    console.log("🛡️ Network Firewall Active");
}

// --- Initialization ---
async function init() {
    try {
        // SECURITY: Install Network Firewall
        installNetworkFirewall();

        setupDOMElements();

        // 1. Load Pyodide
        pyodide = await loadPyodide();
        console.log("Pyodide loaded");

        // 1.1 Pre-load critical packages
        logToTerminal("Instalando librerías (requests, micropip)...", "info");
        await pyodide.loadPackage(["requests", "micropip"]);

        // 1.2 Install PyPI packages
        try {
            const micropip = pyodide.pyimport("micropip");
            logToTerminal("Instalando librerías gráficas (esto puede tardar)...", "info");
            await micropip.install(["py-avataaars", "python-avatars", "svg-turtle", "colorama"]);
        } catch (err) {
            console.warn("Error installing PyPI packages:", err);
            logToTerminal("Advertencia: Algunas librerías gráficas fallaron al instalar.", "info");
        }

        console.log("Packages loaded");

        // Enable Run Button
        const runBtn = document.getElementById("run-code");
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.innerText = "EXECUTE_SCRIPT"; // Updated text
        }

        // 2. Load Exercises
        await loadExercises();

        // 3. Initialize AI System
        aiChat = new AIChat();
        typingSim = new TypingSimulator();
        ttsManager = new TTSManager(); // Initialize TTS

        // Trigger Initial AI Message
        setTimeout(() => {
            if (aiChat) {
                // Force clear history for "Fresh Boot" experience (User Request)
                aiChat.clearHistory();
                aiChat.showWelcomeMessage();
            }
        }, 1500); // Slight delay after load

        // 4. Setup Event Listeners
        setupEventListeners();

        // 5. Load Welcome Lesson
        loadLesson(1);

        // 6. Hide Loader (Success)
        elements.loader.style.display = "none";
        elements.appContainer.style.display = "grid"; // Grid layout
        if (elements.workspaceContainer) elements.workspaceContainer.style.display = "flex";

    } catch (err) {
        console.error("Initialization failed:", err);
        // Ensure loader is visible to show error
        elements.loader.style.display = "flex";
        elements.loader.innerHTML = `<div style="color: #ff7b72; text-align: center; padding: 20px;">
            <h2>❌ Error de Inicio</h2>
            <p>${window.DOMPurify ? window.DOMPurify.sanitize(err.message) : err.message}</p>
            <p style="font-size: 0.8em; color: #8b949e;">Revisa la consola para más detalles.</p>
        </div>`;
    }
}

async function loadExercises() {
    try {
        const response = await fetch(`/static/exercises_v2.json?v=${new Date().getTime()}`);
        if (!response.ok) throw new Error("Failed to load exercises");
        allModules = await response.json();
        // Expose for AI Search
        window.allModules = allModules;
    } catch (error) {
        console.error("Error loading exercises:", error);
        // Optionally, display an error message to the user
        alert("Failed to load exercises. Please try again later.");
    }
    // The LeftPanel class now handles rendering the sidebar, so no direct call here.
}

// --- Sidebar & Navigation ---
// Old renderModuleList removed - replaced by LeftPanel class

function toggleModule(groupElement) {
    const lessons = groupElement.querySelector(".module-lessons");
    lessons.classList.toggle("expanded");
}

function loadLesson(id) {
    // Find lesson
    let foundLesson = null;
    let foundModule = null;
    for (const mod of allModules) {
        const lesson = mod.lessons.find(l => l.id === id);
        if (lesson) {
            foundLesson = lesson;
            foundModule = mod;
            break;
        }
    }

    if (!foundLesson) return;
    currentLesson = foundLesson;
    // Expose for AI Context
    window.currentLesson = currentLesson;

    // Auto-Stop TTS
    if (ttsManager) ttsManager.stop();

    // Update UI
    document.querySelectorAll(".lesson-item").forEach(el => el.classList.remove("active"));

    // Update Editor Header
    // Update Headers
    const editorHeader = document.getElementById("code-editor-header");
    const lessonTitle = document.getElementById("lesson-title");

    if (lessonTitle) {
        lessonTitle.innerText = foundLesson.title.toUpperCase();
    }

    if (editorHeader) {
        editorHeader.innerText = foundLesson.title.toUpperCase();
    }

    // Start Typing Effect
    // Enable run button for skipping
    isTyping = true;
    elements.runBtn.disabled = false;
    elements.runBtn.innerText = "⏩ SKIP";

    typingSim.typeCode(elements.editor, foundLesson.example_code, {
        onChar: () => {
            // Optional: Scroll to bottom or highlight
        },
        onComplete: () => {
            isTyping = false;
            elements.runBtn.disabled = false;
            elements.runBtn.innerText = "EXECUTE_SCRIPT";
        }
    });

    // Clear Terminal
    elements.terminalBody.innerHTML = "";
    logToTerminal("SYSTEM BREACH IN PROGRESS...");
    logToTerminal("Loading module: " + foundLesson.title);
}

// --- Code Execution ---
async function runCode() {
    if (isTyping) {
        typingSim.finish();
        return;
    }

    const code = elements.editor.value;
    logToTerminal("Ejecutando...", "info");

    try {
        // Redirect stdout
        pyodide.setStdout({ batched: (msg) => logToTerminal(msg) });
        await pyodide.runPythonAsync(code);
        logToTerminal("=== Ejecución finalizada ===", "success");
    } catch (err) {
        logToTerminal(err.message, "error");
    }
}

function ansiToHtml(text) {
    if (!text) return text;

    // Basic ANSI to HTML mapping
    const colors = {
        // Foreground
        '30': 'black', '31': '#ff5555', '32': '#50fa7b', '33': '#f1fa8c',
        '34': '#bd93f9', '35': '#ff79c6', '36': '#8be9fd', '37': 'white',
        '90': 'gray', '91': '#ff6e6e', '92': '#69ff94', '93': '#ffffa5',
        '94': '#d6acff', '95': '#ff92df', '96': '#a4ffff', '97': 'white',
        // Background
        '40': 'black', '41': '#ff5555', '42': '#50fa7b', '43': '#f1fa8c',
        '44': '#bd93f9', '45': '#ff79c6', '46': '#8be9fd', '47': 'white'
    };

    // Escape HTML first
    let html = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, ">");

    // Regex for ANSI escape codes: \x1b[...m
    // Capture all codes inside the brackets
    html = html.replace(/\x1b\[([\d;]+)m/g, (match, codesStr) => {
        const codes = codesStr.split(';');
        let style = "";
        let isReset = false;

        codes.forEach(code => {
            if (code === '0') isReset = true;
            if (code === '1') style += "font-weight:bold;";

            if (colors[code]) {
                if (parseInt(code) >= 40 && parseInt(code) <= 47) {
                    style += `background-color:${colors[code]};color:black;`; // Auto-contrast for bg
                } else {
                    style += `color:${colors[code]};`;
                }
            }
        });

        if (isReset) return '</span>';
        return `<span style="${style}">`;
    });

    return html;
}

function logToTerminal(msg, type = "normal") {
    const div = document.createElement("div");

    // Process ANSI codes
    const formattedMsg = ansiToHtml(msg);

    div.innerHTML = `> ${formattedMsg}`;

    if (type === "error") div.classList.add("log-error");
    if (type === "success") div.classList.add("log-success");
    if (type === "info") div.classList.add("log-info");

    elements.terminalBody.appendChild(div);
    elements.terminalBody.scrollTop = elements.terminalBody.scrollHeight;
}

// --- Event Listeners ---
function setupEventListeners() {
    elements.runBtn.onclick = runCode;

    // Editor Tab Support
    elements.editor.addEventListener("keydown", function (e) {
        if (e.key === "Tab") {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + "    " + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 4;
        }
    });

    // Initialize Left Panel
    leftPanel = new LeftPanel(allModules, (lessonId) => loadLesson(lessonId));

    // Close sidebar when clicking a lesson (Mobile)
    if (elements.moduleList) {
        elements.moduleList.addEventListener("click", (e) => {
            if (e.target.classList.contains("lesson-item") && window.innerWidth <= 768) {
                // Optional: Close drawer logic if implemented
            }
        });
    }
}

// --- Clock ---
function updateTime() {
    const timeEl = document.querySelector(".system-time");
    if (!timeEl) return;

    const now = new Date();
    // Madrid Time (CET/CEST)
    const options = {
        timeZone: "Europe/Madrid",
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    };
    const timeString = now.toLocaleTimeString('en-US', options);

    timeEl.innerText = `${timeString} // HACK_TIME`;
}

// Start
init();
setInterval(updateTime, 1000); // Update every second
updateTime(); // Initial call
