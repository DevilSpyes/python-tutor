/**
 * ui_leftpanel.js
 * Manages the left navigation panel, accordion modules, and search filtering.
 */

export class LeftPanel {
    constructor(modules, onSelectLesson) {
        this.modules = modules;
        this.onSelectLesson = onSelectLesson;
        this.container = document.getElementById("module-list");
        this.searchInput = null;
        this.activeModuleId = null;

        this.init();
    }

    init() {
        this.renderSearch();
        this.renderModules();
        this.attachMobileListeners();
    }

    attachMobileListeners() {
        const mobileBtn = document.getElementById("mobile-menu-btn");
        const closeBtn = document.querySelector(".close-sidebar-btn");
        const sidebar = document.querySelector(".col-left");
        const centerCol = document.querySelector(".col-center");

        if (mobileBtn && sidebar) {
            mobileBtn.addEventListener("click", () => {
                sidebar.classList.toggle("active");
            });

            if (closeBtn) {
                closeBtn.addEventListener("click", () => {
                    sidebar.classList.remove("active");
                });
            }

            // Close when clicking outside (on the editor area)
            if (centerCol) {
                centerCol.addEventListener("click", () => {
                    if (window.innerWidth <= 900 && sidebar.classList.contains("active")) {
                        sidebar.classList.remove("active");
                    }
                });
            }
        }
    }

    renderSearch() {
        // Create search container if not exists
        let searchContainer = document.getElementById("panel-search-container");
        if (!searchContainer) {
            searchContainer = document.createElement("div");
            searchContainer.id = "panel-search-container";
            searchContainer.className = "panel-search";
            searchContainer.innerHTML = `
                <input type="text" id="panel-search-input" placeholder="🔍 SEARCH MODULES..." />
            `;
            // Insert before module list
            this.container.parentNode.insertBefore(searchContainer, this.container);

            this.searchInput = document.getElementById("panel-search-input");
            this.searchInput.addEventListener("input", (e) => this.filterContent(e.target.value));
        }
    }

    renderModules() {
        this.container.innerHTML = "";

        this.modules.forEach((mod, index) => {
            const modEl = document.createElement("div");
            modEl.className = "module-group hud-accordion";
            modEl.dataset.id = mod.id;

            // Header
            const header = document.createElement("div");
            header.className = "module-btn";
            header.innerHTML = `
                <span>${mod.title}</span>
            `;
            header.onclick = () => this.toggleModule(mod.id);

            // Lessons Container
            const lessonsContainer = document.createElement("div");
            lessonsContainer.className = "module-lessons";
            lessonsContainer.id = `mod-lessons-${mod.id}`;

            mod.lessons.forEach(lesson => {
                const lessonEl = document.createElement("div");
                lessonEl.className = "lesson-item";
                lessonEl.dataset.id = lesson.id;
                lessonEl.innerHTML = `
                    <span class="lesson-icon">📄</span>
                    <span class="lesson-title">${lesson.title}</span>
                    <span class="status-dot"></span>
                `;
                lessonEl.onclick = (e) => {
                    e.stopPropagation();
                    this.selectLesson(lesson.id);
                };
                lessonsContainer.appendChild(lessonEl);
            });

            modEl.appendChild(header);
            modEl.appendChild(lessonsContainer);
            this.container.appendChild(modEl);
        });
    }

    toggleModule(modId) {
        // Use strict selector to avoid ambiguity
        const modEl = this.container.querySelector(`.module-group[data-id="${modId}"]`);
        if (!modEl) {
            console.error(`Module element not found for ID: ${modId}`);
            return;
        }

        const lessons = modEl.querySelector(".module-lessons");
        if (!lessons) return;

        const isExpanded = lessons.classList.contains("expanded");

        // Toggle current
        if (isExpanded) {
            lessons.classList.remove("expanded");
        } else {
            lessons.classList.add("expanded");
        }
    }

    selectLesson(lessonId) {
        // Highlight UI
        document.querySelectorAll(".lesson-item").forEach(el => el.classList.remove("active"));
        const activeEl = this.container.querySelector(`.lesson-item[data-id="${lessonId}"]`);
        if (activeEl) activeEl.classList.add("active");

        // Callback
        if (this.onSelectLesson) this.onSelectLesson(lessonId);
    }

    filterContent(query) {
        const term = query.toLowerCase().trim();
        const groups = this.container.querySelectorAll(".module-group");

        groups.forEach(group => {
            const modTitle = group.querySelector(".module-btn span").innerText.toLowerCase();
            const lessons = group.querySelectorAll(".lesson-item");
            let hasMatch = false;

            // Check module title match
            const modMatch = modTitle.includes(term);

            // Check lessons
            lessons.forEach(lesson => {
                const lTitle = lesson.querySelector(".lesson-title").innerText.toLowerCase();
                if (lTitle.includes(term) || modMatch) {
                    lesson.style.display = "flex";
                    hasMatch = true;
                } else {
                    lesson.style.display = "none";
                }
            });

            if (hasMatch) {
                group.style.display = "block";
                // Expand if searching and term is not empty
                if (term.length > 0) {
                    group.querySelector(".module-lessons").classList.add("expanded");
                } else {
                    // Collapse if search cleared (optional, or keep state)
                    group.querySelector(".module-lessons").classList.remove("expanded");
                }
            } else {
                group.style.display = "none";
            }
        });
    }
}
