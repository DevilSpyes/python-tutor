/**
 * typingSimulator.js
 * Simulates a "hacker typing" effect for code blocks.
 */

export class TypingSimulator {
    constructor() {
        this.isPaused = false;
        this.speed = 1; // Default speed multiplier
        this.baseDelay = 10; // Base delay in ms (Very Fast)
        this.timeouts = [];
    }

    typeCode(container, code, options = {}) {
        // Clear previous typing
        this.stop();
        container.value = "";

        // Options
        const onComplete = options.onComplete || (() => { });
        const onChar = options.onChar || (() => { });

        let index = 0;
        const totalChars = code.length;

        // Store state for skipping
        this.currentContainer = container;
        this.currentCode = code;
        this.currentOnComplete = onComplete;

        const typeNext = () => {
            if (this.isPaused) return;

            if (index < totalChars) {
                // Add character
                container.value += code[index];
                container.scrollTop = container.scrollHeight; // Auto-scroll
                onChar(index);
                index++;

                // Calculate delay (Hacker feel: random variations)
                let delay = this.baseDelay / this.speed;

                // Randomize slightly for realism
                delay += Math.random() * 30;

                // Pause longer on newlines
                if (code[index - 1] === '\n') delay += 100;

                const timeoutId = setTimeout(typeNext, delay);
                this.timeouts.push(timeoutId);
            } else {
                this.cleanup();
                onComplete();
            }
        };

        // Start typing
        typeNext();
    }

    finish() {
        if (!this.currentCode) return;
        this.stop();
        this.currentContainer.value = this.currentCode;
        this.currentContainer.scrollTop = this.currentContainer.scrollHeight;
        if (this.currentOnComplete) this.currentOnComplete();
        this.cleanup();
    }

    cleanup() {
        this.currentContainer = null;
        this.currentCode = null;
        this.currentOnComplete = null;
    }

    stop() {
        this.timeouts.forEach(clearTimeout);
        this.timeouts = [];
        this.isPaused = false;
    }
}
