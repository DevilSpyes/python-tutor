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

        // Chunking State
        this.chunks = [];
        this.currentChunkIndex = 0;
        this.manualPause = false;

        this.elements = {
            playBtn: null,
            stopBtn: null,
            speedSlider: null,
            speedLabel: null,
            status: null
        };

        this.init();
    }

    // ... (init, loadVoices, renderUI, updateStatus, attachListeners, sanitizeForTTS remain unchanged) ...

    readCurrentExercise() {
        // Anti-Spam: Prevent double clicks
        if (this.isStarting) return;
        this.isStarting = true;

        this.stop(false); // Stop playback, keep UI clean

        const editor = document.querySelector("#code-editor");
        if (!editor) {
            console.warn("TTS: No code editor found.");
            this.isStarting = false;
            return;
        }

        const rawText = editor.value;
        if (!rawText.trim()) {
            console.warn("TTS: Empty text.");
            this.updateStatus("Texto vacío");
            this.isStarting = false;
            return;
        }

        this.updateStatus("Procesando...");
        const cleanText = this.sanitizeForTTS(rawText);

        // CHUNKING: Split text into sentences/logical blocks
        // Split by punctuation followed by space or newline
        this.chunks = cleanText.match(/[^.?!;\n]+[.?!;\n]*/g) || [cleanText];
        this.currentChunkIndex = 0;
        this.manualPause = false;

        // Use pre-selected voice or try to find one again
        if (!this.selectedVoice) {
            this.loadVoices();
        }

        // QUALITY CHECK: Only avoid explicitly "Bad" voices (like espeak)
        const isRoboticVoice = this.selectedVoice && this.selectedVoice.name.toLowerCase().includes('espeak');

        if (isRoboticVoice || !this.selectedVoice) {
            console.warn("TTS: Voice is missing or robotic (espeak). Trying Network Fallback first.");
            // Network fallback doesn't support chunking easily, so we pass full text
            // Ideally we should chunk network too, but for now let's keep it simple
            this.playNetworkAudio(cleanText);
            this.isStarting = false;
            return;
        }

        this.isReading = true;
        this.isPaused = false;
        this.updateButtons();

        this.speakNextChunk();
    }

    speakNextChunk() {
        if (this.currentChunkIndex >= this.chunks.length) {
            // Finished reading all chunks
            this.stop();
            return;
        }

        const textChunk = this.chunks[this.currentChunkIndex];
        console.log(`TTS: Reading chunk ${this.currentChunkIndex + 1}/${this.chunks.length}: "${textChunk.substring(0, 20)}..."`);

        this.speechUtterance = new SpeechSynthesisUtterance(textChunk);

        if (this.selectedVoice) {
            this.speechUtterance.voice = this.selectedVoice;
            this.speechUtterance.lang = this.selectedVoice.lang;
        }

        this.speechUtterance.rate = this.speed;

        this.speechUtterance.onend = () => {
            if (this.manualPause) {
                this.manualPause = false;
                return; // Paused by user, don't advance
            }
            // Chunk finished naturally, move to next
            this.currentChunkIndex++;
            this.speakNextChunk();
        };

        this.speechUtterance.onerror = (e) => {
            console.error("TTS Error:", e);
            if (e.error === 'synthesis-failed' || e.error === 'unavailable') {
                console.warn("TTS: Chunk failed. Trying to skip or fallback...");
                // Try next chunk? Or fallback entire text?
                // Let's try fallback for the REST of the text
                const remainingText = this.chunks.slice(this.currentChunkIndex).join(" ");
                this.playNetworkAudio(remainingText);
                return;
            }
            if (e.error !== 'canceled' && e.error !== 'interrupted') {
                this.stop();
            }
        };

        // Safety delay
        setTimeout(() => {
            try {
                this.synth.speak(this.speechUtterance);
                this.isStarting = false;
            } catch (err) {
                console.error("TTS: Exception calling speak()", err);
                this.isStarting = false;
            }
        }, 50);
    }

    // ... (playNetworkAudio remains unchanged) ...

    pause() {
        if (this.isReading && !this.isPaused) {
            this.manualPause = true;
            this.synth.cancel(); // Stop current chunk
            if (this.audio) {
                this.audio.pause();
            }

            this.isPaused = true;
            this.updateButtons();
            console.log(`TTS: Paused at chunk ${this.currentChunkIndex}`);
        }
    }

    resume() {
        if (this.isReading && this.isPaused) {
            this.isPaused = false;
            this.manualPause = false;
            this.updateButtons();

            // Resume by restarting the current chunk
            if (this.audio) {
                this.audio.play();
            } else {
                this.speakNextChunk();
            }
        }
    }

    stop(resetUI = true) {
        this.synth.cancel();

        if (this.audio) {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.audio = null;
        }

        if (resetUI) {
            this.isReading = false;
            this.isPaused = false;
            this.isStarting = false;
            this.currentChunkIndex = 0;
            this.chunks = [];
            this.updateButtons();
        }
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

        // Filter for Spanish voices
        const spanishVoices = voices.filter(v => v.lang.startsWith('es') || v.lang.includes('es-'));

        if (spanishVoices.length === 0) {
            console.warn("TTS: No Spanish voice found. Using first available.");
            this.selectedVoice = voices[0];
            this.updateStatus("Voz: Sistema (Fallback)");
            return;
        }

        // Priority Sorting:
        // 1. "Premium" (Google, Microsoft, Natural)
        // 2. "Human" names (Andrea, Pedro, Antonio, etc. - common in Linux/SpeechDispatcher)
        // 3. "Generic" human (male, female) but NOT robotic
        // 4. Avoid "Bad" keywords (klatt, robot, espeak, dummy)

        const badKeywords = ['klatt', 'robot', 'espeak', 'dummy', 'network'];
        const humanNames = ['andrea', 'pedro', 'antonio', 'alberto', 'rosa', 'marta', 'monica', 'carlos', 'juan', 'maria', 'helena', 'steph', 'victor'];

        this.selectedVoice = spanishVoices.sort((a, b) => {
            const nameA = a.name.toLowerCase();
            const nameB = b.name.toLowerCase();

            // Tier 1: Premium Cloud Voices
            const aIsPremium = nameA.includes('google') || nameA.includes('microsoft') || nameA.includes('natural');
            const bIsPremium = nameB.includes('google') || nameB.includes('microsoft') || nameB.includes('natural');
            if (aIsPremium && !bIsPremium) return -1;
            if (!aIsPremium && bIsPremium) return 1;

            // Tier 2: Specific Human Names (Best for Local Linux)
            const aIsHuman = humanNames.some(n => nameA.includes(n));
            const bIsHuman = humanNames.some(n => nameB.includes(n));
            if (aIsHuman && !bIsHuman) return -1;
            if (!aIsHuman && bIsHuman) return 1;

            // Tier 3: Avoid "Bad" / Robotic Voices
            const aIsBad = badKeywords.some(k => nameA.includes(k));
            const bIsBad = badKeywords.some(k => nameB.includes(k));
            if (!aIsBad && bIsBad) return -1;
            if (aIsBad && !bIsBad) return 1;

            return 0;
        })[0];

        if (this.selectedVoice) {
            console.log("TTS: Selected Voice:", this.selectedVoice.name);
            this.updateStatus("Voz: " + this.selectedVoice.name.substring(0, 15) + "...");
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
                <span id="tts-status" class="tts-status" style="font-size: 10px; color: #0f0; margin-left: 10px;">Init...</span>
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
            if (this.isReading && !this.isPaused) {
                this.pause();
            } else if (this.isPaused) {
                this.resume();
            } else {
                this.readCurrentExercise();
            }
        });

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
            .replace(/==/g, " igual a ")
            .replace(/!=/g, " distinto de ")
            .replace(/>=/g, " mayor o igual a ")
            .replace(/<=/g, " menor o igual a ")
            .replace(/=/g, " asigna ")
            .replace(/\+/g, " más ")
            //.replace(/-/g, " menos ") // Context dependent, maybe keep as is or space
            .replace(/\*/g, " por ")
            .replace(/\//g, " entre ")
            .replace(/_/g, " ")         // snake_case -> snake case
            // Remove noisy symbols, replace with slight pauses (commas or spaces)
            .replace(/[(){}\[\]:;"']/g, " ")
            .replace(/\s+/g, " ")       // Collapse multiple spaces
            .trim();
    }

    readCurrentExercise(startOffset = 0) {
        // Anti-Spam: Prevent double clicks
        if (this.isStarting) return;
        this.isStarting = true;

        this.stop(false); // Stop playback, but don't reset UI if we are just restarting

        const editor = document.querySelector("#code-editor");
        if (!editor) {
            console.warn("TTS: No code editor found.");
            this.isStarting = false;
            return;
        }

        const rawText = editor.value;
        if (!rawText.trim()) {
            console.warn("TTS: Empty text.");
            this.updateStatus("Texto vacío");
            this.isStarting = false;
            return;
        }

        this.updateStatus("Procesando...");
        let cleanText = this.sanitizeForTTS(rawText);

        // Resume Logic: Slice text if offset is provided
        if (startOffset > 0 && startOffset < cleanText.length) {
            cleanText = cleanText.substring(startOffset);
            console.log(`TTS: Resuming from index ${startOffset}`);
        } else {
            this.lastCharIndex = 0; // Reset if starting fresh
        }

        // Use pre-selected voice or try to find one again
        if (!this.selectedVoice) {
            this.loadVoices();
        }

        // QUALITY CHECK: Only avoid explicitly "Bad" voices (like espeak)
        const isRoboticVoice = this.selectedVoice && this.selectedVoice.name.toLowerCase().includes('espeak');

        if (isRoboticVoice || !this.selectedVoice) {
            console.warn("TTS: Voice is missing or robotic (espeak). Trying Network Fallback first.");
            this.playNetworkAudio(cleanText);
            this.isStarting = false;
            return;
        }

        this.speakNative(cleanText);
    }

    speakNative(text, force = false) {
        if (!this.selectedVoice && !force) {
            console.warn("TTS: No voice to speak native.");
            return;
        }

        this.speechUtterance = new SpeechSynthesisUtterance(text);

        if (this.selectedVoice) {
            this.speechUtterance.voice = this.selectedVoice;
            this.speechUtterance.lang = this.selectedVoice.lang;
        } else if (force) {
            console.warn("TTS: Forcing native speech with system default.");
        }

        this.speechUtterance.rate = this.speed;

        this.baseOffset = this.lastCharIndex || 0; // Start of this chunk relative to full text

        this.speechUtterance.onboundary = (event) => {
            this.lastCharIndex = this.baseOffset + event.charIndex;
        };

        this.speechUtterance.onend = () => {
            if (this.manualPause) {
                this.manualPause = false;
                return; // Ignore onend if we manually paused
            }
            this.isReading = false;
            this.isPaused = false;
            this.lastCharIndex = 0;
            this.updateButtons();
        };

        this.speechUtterance.onerror = (e) => {
            console.error("TTS Error:", e);
            if (e.error === 'synthesis-failed' || e.error === 'unavailable') {
                if (!force) {
                    console.warn("TTS: Native synthesis failed. Trying lightweight network fallback...");
                    this.playNetworkAudio(text);
                } else {
                    this.updateStatus("Error: TTS Falló");
                    this.isReading = false;
                    this.updateButtons();
                }
                return;
            }
            if (e.error !== 'canceled' && e.error !== 'interrupted') {
                this.isReading = false;
                this.isPaused = false;
                this.updateButtons();
            }
        };

        this.isReading = true;
        this.isPaused = false;
        this.updateButtons();

        // Safety delay
        setTimeout(() => {
            try {
                this.synth.speak(this.speechUtterance);
                this.isStarting = false; // Release lock
            } catch (err) {
                console.error("TTS: Exception calling speak()", err);
                if (!force) {
                    this.playNetworkAudio(text);
                }
                this.isStarting = false;
            }
        }, 100);
    }

    playNetworkAudio(text) {
        this.stop(false); // Ensure clean slate, but don't reset UI state

        // Lightweight fallback (No AI, just a GET request)
        const googleUrl = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=es&q=${encodeURIComponent(text)}`;

        this.audio = new Audio(googleUrl);
        this.audio.playbackRate = this.speed;

        this.audio.onended = () => {
            this.isReading = false;
            this.isPaused = false;
            this.updateButtons();
        };

        this.audio.onerror = (e) => {
            console.error("TTS: Network audio failed", e);

            // TIER 3 FALLBACK: Always try Robotic Native Voice as last resort
            // Even if no voice was found in getVoices(), browser might have a default.
            console.warn("TTS: Network failed. Falling back to Absolute System Default (Last Resort).");
            this.updateStatus("Voz: Sistema (Robótica)");
            this.speakNative(text, true); // Force native
        };

        this.audio.play()
            .then(() => {
                this.isReading = true;
                this.isPaused = false;
                this.updateButtons();
                this.updateStatus("Voz: Red (Fallback)");
            })
            .catch(e => {
                console.error("TTS: Playback error", e);
                // Trigger onerror logic manually if play fails immediately
                this.audio.onerror(e);
            });
    }

    pause() {
        if (this.isReading && !this.isPaused) {
            // SOFT PAUSE: Cancel playback but remember position
            this.manualPause = true; // Flag to ignore onend
            this.synth.cancel();
            if (this.audio) {
                this.audio.pause();
            }

            this.isPaused = true;
            this.updateButtons();
            console.log(`TTS: Paused at index ${this.lastCharIndex}`);
        }
    }

    resume() {
        if (this.isReading && this.isPaused) {
            // SOFT RESUME: Restart from last index
            this.isPaused = false;
            this.readCurrentExercise(this.lastCharIndex);
        }
    }

    stop(resetUI = true) {
        // Native
        this.synth.cancel();

        // Fallback
        if (this.audio) {
            this.audio.pause();
            this.audio.currentTime = 0; // Reset
            this.audio = null;
        }

        if (resetUI) {
            this.isReading = false;
            this.isPaused = false;
            this.lastCharIndex = 0;
            this.isStarting = false; // Force unlock
            this.updateButtons();
        }
    }

    updateButtons() {
        if (!this.elements.playBtn) return;

        if (this.isReading && !this.isPaused) {
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
