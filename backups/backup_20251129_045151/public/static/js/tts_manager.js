/**
 * tts_manager.js
 * Manages Audio Playback for the Code Editor using pre-generated MP3 files.
 */

export class TTSManager {
    constructor() {
        this.audio = null;
        this.isPlaying = false;
        this.isPaused = false;
        this.speed = 1.0;
        this.container = null;
        this.manifest = null;

        this.elements = {
            playBtn: null,
            stopBtn: null,
            speedSlider: null,
            speedLabel: null,
            status: null
        };

        this.init();
    }

    async init() {
        console.log("TTS: Initializing (Audio File Mode)...");
        this.renderUI();
        this.attachListeners();

        try {
            const response = await fetch('/audio/manifest.json');
            if (response.ok) {
                this.manifest = await response.json();
                console.log("TTS: Audio manifest loaded.");
                this.updateStatus("Sistema de Voz Listo");
            } else {
                console.error("TTS: Failed to load manifest.json");
                this.updateStatus("Error: Manifest no encontrado");
            }
        } catch (e) {
            console.error("TTS: Error loading manifest", e);
            this.updateStatus("Error: Fallo de Red");
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
                <button id="tts-stop" class="tts-btn" title="Detener">⏹</button>
                <div class="tts-speed-control">
                    <span class="tts-label">SPEED:</span>
                    <input type="range" id="tts-speed" min="0.5" max="2.0" step="0.1" value="1.0">
                    <span id="tts-speed-val" class="tts-val">1.0x</span>
                </div>
                <span id="tts-status" class="tts-status" style="font-size: 10px; color: #0f0; margin-left: 10px;">Cargando Voz...</span>
            </div>
        `;

        footerBar.innerHTML = '';
        footerBar.appendChild(this.container);

        this.elements.playBtn = this.container.querySelector('#tts-play');
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
            if (this.isPlaying && !this.isPaused) {
                this.pause();
            } else if (this.isPaused) {
                this.resume();
            } else {
                this.playCurrentLesson();
            }
        });

        this.elements.stopBtn.addEventListener('click', () => this.stop());

        this.elements.speedSlider.addEventListener('input', (e) => {
            this.speed = parseFloat(e.target.value);
            this.elements.speedLabel.innerText = `${this.speed.toFixed(1)}x`;
            if (this.audio) {
                this.audio.playbackRate = this.speed;
            }
        });
    }

    playCurrentLesson() {
        if (!this.manifest) {
            console.warn("TTS: Manifest not loaded yet.");
            return;
        }

        const currentLesson = window.currentLesson;
        if (!currentLesson) {
            console.warn("TTS: No lesson selected.");
            this.updateStatus("Selecciona una lección");
            return;
        }

        const filename = this.manifest[currentLesson.id];
        if (!filename) {
            console.warn(`TTS: No audio file found for lesson ID ${currentLesson.id}`);
            this.updateStatus("Audio no disponible");
            return;
        }

        this.stop(false); // Stop any current playback

        const audioPath = `/audio/${filename}`;
        console.log(`TTS: Playing ${audioPath}`);
        this.updateStatus("Reproduciendo...");

        this.audio = new Audio(audioPath);
        this.audio.playbackRate = this.speed;

        this.audio.onended = () => {
            this.isPlaying = false;
            this.isPaused = false;
            this.updateButtons();
            this.updateStatus("Voz: Lista");
        };

        this.audio.onerror = (e) => {
            console.error("TTS: Audio playback error", e);
            this.updateStatus("Error de Reproducción");
            this.isPlaying = false;
            this.updateButtons();
        };

        this.audio.play()
            .then(() => {
                this.isPlaying = true;
                this.isPaused = false;
                this.updateButtons();
            })
            .catch(e => {
                console.error("TTS: Play failed", e);
                this.updateStatus("Error al iniciar");
            });
    }

    pause() {
        if (this.audio && this.isPlaying && !this.isPaused) {
            this.audio.pause();
            this.isPaused = true;
            this.updateButtons();
            this.updateStatus("Pausado");
        }
    }

    resume() {
        if (this.audio && this.isPaused) {
            this.audio.play();
            this.isPaused = false;
            this.updateButtons();
            this.updateStatus("Reproduciendo...");
        }
    }

    stop(resetUI = true) {
        if (this.audio) {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.audio = null;
        }

        if (resetUI) {
            this.isPlaying = false;
            this.isPaused = false;
            this.updateButtons();
            this.updateStatus("Voz: Lista");
        }
    }

    updateButtons() {
        if (!this.elements.playBtn) return;

        if (this.isPlaying && !this.isPaused) {
            // State: Playing -> Show Pause Icon
            this.elements.playBtn.innerText = "⏸";
            this.elements.playBtn.title = "Pausar";
        } else {
            // State: Paused or Stopped -> Show Play Icon
            this.elements.playBtn.innerText = "▶";
            this.elements.playBtn.title = this.isPaused ? "Reanudar" : "Leer ejercicio";
        }
    }
}
