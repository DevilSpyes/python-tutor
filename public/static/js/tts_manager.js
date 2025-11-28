/**
 * tts_manager.js
 * Manages Text-to-Speech functionality for the Code Editor.
 */

export class TTSManager {
    constructor() {
        this.synth = window.speechSynthesis;
        this.speechUtterance = null;
        this.isReading = false;
        this.isPaused = false;
        this.speed = 1.0;
        this.container = null;

        this.elements = {
            playBtn: null,
            pauseBtn: null,
            stopBtn: null,
            speedSlider: null,
            speedLabel: null,
            status: null
        };

        this.init();
    }

    async init() {
        console.log("TTS: Initializing (Native Mode)...");
        this.renderUI();
        this.attachListeners();

        // Wake up call
        this.synth.cancel();

        // Polling for voices (Aggressive strategy for Linux/Chrome)
        let attempts = 0;
        const maxAttempts = 50; // 5 seconds

        const loadVoicesTimer = setInterval(() => {
            const voices = this.synth.getVoices();
            if (voices.length > 0) {
                clearInterval(loadVoicesTimer);
                this.loadVoices();
            } else {
                attempts++;
                if (attempts >= maxAttempts) {
                    clearInterval(loadVoicesTimer);
                    console.warn("TTS: Timeout waiting for voices.");
                    this.updateStatus("Voz: Default");
                }
            }
        }, 100);

        // Also listen for event
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = () => this.loadVoices();
        }

        this.updateStatus("Voz Nativa Lista");
    }

    loadVoices() {
        const voices = this.synth.getVoices();
        if (voices.length === 0) return;

        console.log("TTS: Available Voices:", voices.map(v => `${v.name} (${v.lang})`).join(", "));

        // Priority: Google Spanish -> Any Spanish -> Any Voice
        this.selectedVoice = voices.find(v => v.lang.startsWith('es') && v.name.includes('Google')) ||
            voices.find(v => v.lang.startsWith('es')) ||
            voices.find(v => v.lang.includes('es'));

        if (this.selectedVoice) {
            console.log("TTS: Selected Voice:", this.selectedVoice.name);
            this.updateStatus("Voz: " + this.selectedVoice.name.substring(0, 15) + "...");
        } else {
            console.warn("TTS: No Spanish voice found. Using first available.");
            this.selectedVoice = voices[0]; // Fallback to ANY voice
            this.updateStatus("Voz: Sistema (Fallback)");
        }
    }

    renderUI() {
        const footerBar = document.querySelector('.editor-window .window-footer-bar');
        if (!footerBar) return;

        this.container = document.createElement('div');
        this.container.className = 'tts-panel';
        this.container.innerHTML = `
            <div class="tts-controls">
                <button id="tts-play" class="tts-btn" title="Leer ejercicio">▶</button>
                <button id="tts-pause" class="tts-btn" title="Pausar" style="display:none;">⏸</button>
                <button id="tts-stop" class="tts-btn" title="Detener">⏹</button>
                <div class="tts-speed-control">
                    <span class="tts-label">SPEED:</span>
                    <input type="range" id="tts-speed" min="0.5" max="2.0" step="0.1" value="1.0">
                    <span id="tts-speed-val" class="tts-val">1.0x</span>
                </div>
                <span id="tts-status" class="tts-status" style="font-size: 10px; color: #0f0; margin-left: 10px;">Init...</span>
            </div>
        `;

        footerBar.innerHTML = '';
        footerBar.appendChild(this.container);

        this.elements.playBtn = this.container.querySelector('#tts-play');
        this.elements.pauseBtn = this.container.querySelector('#tts-pause');
        this.elements.stopBtn = this.container.querySelector('#tts-stop');
        this.elements.speedSlider = this.container.querySelector('#tts-speed');
        this.elements.speedLabel = this.container.querySelector('#tts-speed-val');
        this.elements.status = this.container.querySelector('#tts-status');
    }

    updateStatus(msg) {
        if (this.elements.status) this.elements.status.innerText = msg;
    }

    attachListeners() {
        if (!this.container) return;

        this.elements.playBtn.addEventListener('click', () => {
            if (this.isPaused) {
                this.resume();
            } else {
                this.readCurrentExercise();
            }
        });

        this.elements.pauseBtn.addEventListener('click', () => this.pause());
        this.elements.stopBtn.addEventListener('click', () => this.stop());

        this.elements.speedSlider.addEventListener('input', (e) => {
            this.speed = parseFloat(e.target.value);
            this.elements.speedLabel.innerText = `${this.speed.toFixed(1)}x`;
            if (this.speechUtterance) {
                this.speechUtterance.rate = this.speed;
            }
        });
    }

    sanitizeForTTS(text) {
        return text
            .replace(/^#\s?/gm, "")     // quitar # al inicio
            .replace(/#/g, "")          // eliminar # restantes
            .replace(/==/g, " igual igual ")
            .replace(/=/g, " igual ")
            .replace(/:/g, " dos puntos ")
            .replace(/\(/g, " abre paréntesis ")
            .replace(/\)/g, " cierra paréntesis ")
            .replace(/{/g, " llave abre ")
            .replace(/}/g, " llave cierra ");
    }

    readCurrentExercise() {
        this.stop(); // cancelar cualquier lectura previa

        const editor = document.querySelector("#code-editor");
        if (!editor) {
            console.warn("TTS: No code editor found.");
            return;
        }

        const rawText = editor.value;
        if (!rawText.trim()) {
            console.warn("TTS: Empty text.");
            return;
        }

        const cleanText = this.sanitizeForTTS(rawText);

        this.speechUtterance = new SpeechSynthesisUtterance(cleanText);

        // Use pre-selected voice or try to find one again
        if (!this.selectedVoice) {
            this.loadVoices();
        }

        if (this.selectedVoice) {
            this.speechUtterance.voice = this.selectedVoice;
            this.speechUtterance.lang = this.selectedVoice.lang;
        } else {
            // Fallback: Do NOT force lang if no voices found, let browser default
            console.warn("TTS: No Spanish voice found. Letting browser decide default.");
            // this.speechUtterance.lang = "es-ES"; // Commented out to avoid synthesis-failed
        }

        this.speechUtterance.rate = this.speed;

        this.speechUtterance.onend = () => {
            this.isReading = false;
            this.isPaused = false;
            this.updateButtons();
        };

        this.speechUtterance.onerror = (e) => {
            console.error("TTS Error:", e);
            if (e.error === 'synthesis-failed' || e.error === 'unavailable') {
                console.warn("TTS: Native synthesis failed. Trying lightweight network fallback...");
                this.playNetworkAudio(cleanText);
                return;
            }
            this.isReading = false;
            this.isPaused = false;
            this.updateButtons();
        };

        this.isReading = true;
        this.isPaused = false;
        this.updateButtons();

        // Safety delay
        setTimeout(() => {
            try {
                this.synth.speak(this.speechUtterance);
            } catch (err) {
                console.error("TTS: Exception calling speak()", err);
                this.playNetworkAudio(cleanText);
            }
        }, 100);
    }

    playNetworkAudio(text) {
        // Lightweight fallback (No AI, just a GET request)
        const googleUrl = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=es&q=${encodeURIComponent(text)}`;

        if (this.audio) {
            this.audio.pause();
            this.audio = null;
        }

        this.audio = new Audio(googleUrl);
        this.audio.playbackRate = this.speed;

        this.audio.onended = () => {
            this.isReading = false;
            this.isPaused = false;
            this.updateButtons();
        };

        this.audio.onerror = (e) => {
            console.error("TTS: Network audio failed", e);
            this.updateStatus("Error: TTS no disponible");
            this.isReading = false;
            this.isPaused = false;
            this.updateButtons();
        };

        this.audio.play().catch(e => console.error("TTS: Playback error", e));
        this.updateStatus("Voz: Red (Fallback)");
    }

    pause() {
        if (this.synth.speaking && !this.synth.paused) {
            this.synth.pause();
            this.isPaused = true;
            this.updateButtons();
        }
    }

    resume() {
        if (this.synth.paused) {
            this.synth.resume();
            this.isPaused = false;
            this.updateButtons();
        }
    }

    stop() {
        this.synth.cancel();
        this.isReading = false;
        this.isPaused = false;
        this.updateButtons();
    }

    updateButtons() {
        if (this.isReading && !this.isPaused) {
            this.elements.playBtn.style.display = 'none';
            this.elements.pauseBtn.style.display = 'inline-block';
        } else {
            this.elements.playBtn.style.display = 'inline-block';
            this.elements.pauseBtn.style.display = 'none';
        }
    }
}
