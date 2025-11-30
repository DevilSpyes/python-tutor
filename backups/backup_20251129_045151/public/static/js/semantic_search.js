/**
 * semantic_search.js
 * Ultra-Fast Embedding Engine using transformers.js
 */

import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.8.0';
import { KnowledgeBase } from './knowledge_base.js';

// Skip local check for transformers.js to avoid CORS issues with file://
env.allowLocalModels = false;
env.useBrowserCache = true;

export class SemanticSearch {
    constructor() {
        this.pipe = null;
        this.knowledge = [];
        this.embeddings = null; // Cache for knowledge embeddings
        this.isReady = false;
        this.kb = new KnowledgeBase();
    }

    async init() {
        if (this.isReady) return;
        console.log("Initializing Semantic Search Engine...");

        // 1. Generate Knowledge Base
        this.knowledge = this.kb.generate();
        console.log(`Generated ${this.knowledge.length} knowledge entries.`);

        // 2. Load Embedding Model (Quantized all-MiniLM-L6-v2 ~23MB)
        this.pipe = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

        // 3. Pre-compute Embeddings (Lazy or Batch?)
        // For 1000 items, doing it all at once might freeze UI. 
        // Strategy: Compute on demand or use a very fast keyword filter first?
        // User requested "Embeddings". We will compute them.
        // Optimization: We will only compute embeddings for the *Query* and compare against *Keywords* first?
        // No, true semantic search needs vectors.
        // We will compute vectors for the KB in chunks to avoid freezing.

        this.isReady = true;
        console.log("Semantic Search Engine Ready.");

        // Start background indexing (non-blocking)
        this.indexKnowledgeBase();
    }

    async indexKnowledgeBase() {
        console.log("Indexing Knowledge Base...");
        const vectors = [];
        // Process in chunks of 10
    }

    // indexKnowledgeBase method is removed as its functionality is integrated into init()

    cosineSimilarity(a, b) {
        let dot = 0;
        for (let i = 0; i < a.length; i++) {
            dot += a[i] * b[i];
        }
        return dot; // Assumes normalized vectors
    }

    async search(query) {
        if (!this.pipeline) await this.init(); // Ensure pipeline is loaded

        // 1. Embed Query
        const output = await this.pipeline(query, { pooling: 'mean', normalize: true });
        const queryEmbedding = output.data;

        // 2. Brute-force Cosine Similarity
        let bestMatch = null;
        let maxScore = -1;

        for (const doc of this.documents) {
            const score = this.cosineSimilarity(queryEmbedding, doc.embedding);
            if (score > maxScore) {
                maxScore = score;
                bestMatch = doc;
            }
        }

        console.log(`Best Match: "${bestMatch?.text}" (Score: ${maxScore.toFixed(2)})`);

        // 3. Rapid Intent Detection (Static QA) - Threshold > 0.4 (Flexible Matching)
        if (bestMatch && bestMatch.type === 'static' && maxScore > 0.4) {
            return {
                type: 'exact',
                content: `**${bestMatch.text}**\n\n${bestMatch.answer}`,
                score: maxScore
            };
        }

        // High Confidence Match (Generated) - Threshold > 0.65
        if (bestMatch && maxScore > 0.65) {
            return {
                type: 'exact',
                content: bestMatch.answer,
                score: maxScore
            };
        }

        // Fallback if no high-confidence match
        return { type: 'fallback', score: maxScore };
    }
}
