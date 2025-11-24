import { AIChat } from "./ai_chat.js";

// Global State
let pyodide = null;
let currentLessonId = 1;
let currentLesson = null;
let allModules = [];
let aiChat = null; // New AI Controller

// DOM Elements
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
        settingsBtn: document.getElementById("settings-btn"),
        settingsModal: document.getElementById("settings-modal"),
        closeSettings: document.getElementById("close-settings"),
        saveSettings: document.getElementById("save-settings"),
        apiKeyInput: document.getElementById("api-key"),
        providerSelect: document.getElementById("ai-provider")
    };

    // Debugging: Check for missing critical elements
    if (!elements.loader) console.error("CRITICAL: #initial-loader not found!");
    if (!elements.appContainer) console.error("CRITICAL: #app-container not found!");
}

// --- Initialization ---
async function init() {
    try {
        setupDOMElements();

        // 1. Load Pyodide
        pyodide = await loadPyodide();
        console.log("Pyodide loaded");

        // Enable Run Button
        const runBtn = document.getElementById("run-code");
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.innerText = "▶ Ejecutar";
        }

        // 2. Load Exercises
        await loadExercises();

        // 3. Initialize AI System
        aiChat = new AIChat();

        // 4. Setup Event Listeners
        setupEventListeners();

        // 5. Load Welcome Lesson
        loadLesson(1);

        // 6. Hide Loader (Success)
        elements.loader.style.display = "none";
        elements.appContainer.style.display = "flex";
        if (elements.workspaceContainer) elements.workspaceContainer.style.display = "flex";

    } catch (err) {
        console.error("Initialization failed:", err);
        // Ensure loader is visible to show error
        elements.loader.style.display = "flex";
        elements.loader.innerHTML = `<div style="color: #ff7b72; text-align: center; padding: 20px;">
            <h2>❌ Error de Inicio</h2>
            <p>${err.message}</p>
            <p style="font-size: 0.8em; color: #8b949e;">Revisa la consola para más detalles.</p>
        </div>`;
    }
}

async function loadExercises() {
    const response = await fetch("/static/exercises.json");
    allModules = await response.json();
    renderSidebar();
}

// --- Sidebar & Navigation ---
function renderSidebar() {
    elements.moduleList.innerHTML = "";

    allModules.forEach(module => {
        const group = document.createElement("div");
        group.className = "module-group";

        const header = document.createElement("div");
        header.className = "module-header";
        header.innerText = module.title;
        header.onclick = () => toggleModule(group);

        const lessonsContainer = document.createElement("div");
        lessonsContainer.className = "module-lessons";

        module.lessons.forEach(lesson => {
            const item = document.createElement("div");
            item.className = "lesson-item";
            item.innerText = lesson.title;
            item.onclick = () => loadLesson(lesson.id);
            lessonsContainer.appendChild(item);
        });

        group.appendChild(header);
        group.appendChild(lessonsContainer);
        elements.moduleList.appendChild(group);
    });
}

function toggleModule(groupElement) {
    const lessons = groupElement.querySelector(".module-lessons");
    lessons.classList.toggle("expanded");
}

function loadLesson(id) {
    // Find lesson
    let foundLesson = null;
    for (const mod of allModules) {
        const lesson = mod.lessons.find(l => l.id === id);
        if (lesson) {
            foundLesson = lesson;
            break;
        }
    }

    if (!foundLesson) return;
    currentLesson = foundLesson;

    // Update UI
    document.querySelectorAll(".lesson-item").forEach(el => el.classList.remove("active"));
    // Highlight active (simple check by text for now, or add ID to element)

    // Render Content
    if (elements.lessonTitle) elements.lessonTitle.innerText = foundLesson.title;
    elements.lessonContent.innerHTML = window.marked ? window.marked.parse(foundLesson.content) : foundLesson.content;
    elements.editor.value = foundLesson.example_code;

    // Clear Terminal
    elements.terminalBody.innerHTML = "";
    logToTerminal("Lección cargada: " + foundLesson.title);
}

// --- Code Execution ---
async function runCode() {
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

function logToTerminal(msg, type = "normal") {
    const div = document.createElement("div");
    div.innerText = `> ${msg}`;
    if (type === "error") div.style.color = "#ff7b72";
    if (type === "success") div.style.color = "#2ea043";
    if (type === "info") div.style.color = "#58a6ff";
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

    // Mobile Navigation Logic
    const sidebar = document.getElementById("sidebar");
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    const closeSidebarBtn = document.getElementById("close-sidebar-btn");
    const mobileChatBtn = document.getElementById("mobile-chat-btn");
    const aiPanel = document.querySelector(".ai-panel");

    if (mobileMenuBtn) {
        mobileMenuBtn.onclick = () => {
            sidebar.classList.add("active");
        };
    }

    if (closeSidebarBtn) {
        closeSidebarBtn.onclick = () => {
            sidebar.classList.remove("active");
        };
    }

    if (mobileChatBtn) {
        mobileChatBtn.onclick = () => {
            // Toggle AI Panel
            if (aiPanel.classList.contains("active")) {
                aiPanel.classList.remove("active");
            } else {
                aiPanel.classList.add("active");
            }
        };
    }

    const closeAiBtn = document.getElementById("close-ai-btn");
    if (closeAiBtn) {
        closeAiBtn.onclick = () => {
            aiPanel.classList.remove("active");
        };
    }

    // Close sidebar when clicking a lesson
    document.getElementById("module-list").addEventListener("click", (e) => {
        if (e.target.classList.contains("lesson-item") && window.innerWidth <= 768) {
            sidebar.classList.remove("active");
        }
    });
}

// Start
init();
