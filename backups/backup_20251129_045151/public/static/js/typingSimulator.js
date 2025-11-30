/**
 * typingSimulator.js
 * Simulates a "hacker typing" effect for code blocks.
 */

export class TypingSimulator {
    constructor() {
        this.currentContainer = null;
        this.currentCode = null;
        this.currentOnComplete = null;

        // Internal state for the new logic
        this._timer = null;
        this._interactionTimer = null;
        this._index = 0;
        this._isRunning = false;
        this._userInteracting = false;

        // Configuration
        this.speed = 30;
        this.autoScroll = true;
        this.resumeAfter = 1200;
    }

    typeCode(container, code, options = {}) {
        // Stop any previous typing
        this.stop();

        this.currentContainer = container;
        this.currentCode = code;
        this.currentOnComplete = options.onComplete || (() => { });
        const onChar = options.onChar || (() => { });

        // Clear container
        container.value = "";
        this._index = 0;
        this._isRunning = true;
        this._userInteracting = false;

        // Setup scroll listener for this specific container
        // We need to bind the listener to remove it later or handle it correctly
        // For simplicity in this singleton-like usage, we'll attach a new one
        // Note: In a stricter environment we might want to clean up old listeners,
        // but given the app structure, this is acceptable if we manage the flag correctly.

        // Remove old listener if exists (hacky but safe for this specific app context)
        if (container._scrollHandler) {
            container.removeEventListener('scroll', container._scrollHandler);
        }

        container._scrollHandler = () => {
            if (!this._isRunning) return;

            // Ignore scroll events triggered by our own auto-scroll
            if (this._isAutoScrolling) {
                this._isAutoScrolling = false; // Reset flag
                return;
            }

            this._userInteracting = true;
            if (this._interactionTimer) clearTimeout(this._interactionTimer);
            this._interactionTimer = setTimeout(() => {
                this._userInteracting = false;
            }, this.resumeAfter);
        };

        container.addEventListener('scroll', container._scrollHandler);

        // Start typing loop
        this._timer = setInterval(() => {
            if (!this._isRunning) return;

            if (this._index >= this.currentCode.length) {
                this.finish(); // Use finish to ensure clean completion
                return;
            }

            this._index++;
            container.value = this.currentCode.slice(0, this._index);

            // Auto-scroll logic
            if (this.autoScroll && !this._userInteracting) {
                this._isAutoScrolling = true; // Set flag before scrolling
                container.scrollTop = container.scrollHeight;
            }

            onChar(this._index);

        }, this.speed);
    }

    finish() {
        if (!this.currentCode) return;

        // Stop the timer but keep the logic to fill text
        this._isRunning = false;
        if (this._timer) clearInterval(this._timer);
        if (this._interactionTimer) clearTimeout(this._interactionTimer);

        // Fill remaining text
        this.currentContainer.value = this.currentCode;

        // Force scroll to bottom on finish
        this.currentContainer.scrollTop = this.currentContainer.scrollHeight;

        // Cleanup listener
        if (this.currentContainer && this.currentContainer._scrollHandler) {
            this.currentContainer.removeEventListener('scroll', this.currentContainer._scrollHandler);
            delete this.currentContainer._scrollHandler;
        }

        // Callback
        if (this.currentOnComplete) this.currentOnComplete();

        this.cleanup();
    }

    stop() {
        this._isRunning = false;
        if (this._timer) clearInterval(this._timer);
        if (this._interactionTimer) clearTimeout(this._interactionTimer);

        // Cleanup listener if we stopped mid-way
        if (this.currentContainer && this.currentContainer._scrollHandler) {
            this.currentContainer.removeEventListener('scroll', this.currentContainer._scrollHandler);
            delete this.currentContainer._scrollHandler;
        }
    }

    cleanup() {
        this.currentContainer = null;
        this.currentCode = null;
        this.currentOnComplete = null;
        this._index = 0;
    }
}
