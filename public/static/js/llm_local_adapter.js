/**
 * llm_local_adapter.js
 * Unified Adapter for "Chat Professor Lite" (Rule-Based System).
 * Replaces previous AI adapters.
 */

/*
// --- OLD ADAPTERS (DISABLED) ---
// export class LocalOfflineAdapter { ... }
// export class LocalGGUFAdapter { ... }
*/

export class ProfessorLiteAdapter {
    constructor() {
        this.status = {
            loaded: false,
            model: "Professor Lite (Rule-Based)",
            device: 'cpu'
        };
        this.knowledgeBase = null;
        this.exercises = null;
        this.glossary = null; // New Glossary
    }

    async loadModel(config = {}) {
        if (this.status.loaded) return true;

        console.log("Loading Professor Lite Knowledge Base...");
        if (config.onProgress) config.onProgress({ status: 'init', progress: 0, message: 'Cargando base de conocimiento...' });

        try {
            // Load the Lite Knowledge Base
            const kbResponse = await fetch('/static/js/knowledge_base_lite.json');
            if (!kbResponse.ok) throw new Error(`Failed to load KB: ${kbResponse.status}`);
            this.knowledgeBase = await kbResponse.json();

            // Load the Exercises DB (for fallback info)
            const exResponse = await fetch('/static/exercises_v2.json');
            if (!exResponse.ok) throw new Error(`Failed to load Exercises: ${exResponse.status}`);
            this.exercises = await exResponse.json();

            // Load the Glossary
            const glosResponse = await fetch('/static/js/glossary.json');
            if (!glosResponse.ok) {
                console.warn("Glossary not found, using empty.");
                this.glossary = {};
            } else {
                this.glossary = await glosResponse.json();
            }

            this.status.loaded = true;
            console.log("Professor Lite Ready!");
            if (config.onProgress) config.onProgress({ status: 'ready', progress: 100, message: '¡Profesor listo!' });
            return true;
        } catch (e) {
            console.error("Failed to load knowledge base:", e);
            throw e;
        }
    }

    async sendMessage(history, context, callbacks = {}) {
        if (!this.status.loaded) throw new Error("Professor Lite not loaded");

        const userMessage = history[history.length - 1].content;

        // Check for Referenced Context (Module or Lesson) - High Priority
        const refModuleSummary = this._extractReferencedModule(context);
        if (refModuleSummary) {
            await this._streamResponse(refModuleSummary, callbacks);
            return { text: refModuleSummary };
        }

        let exerciseId = this._extractReferencedLessonId(context);
        if (!exerciseId) {
            exerciseId = this._extractExerciseId(context);
        }

        const exerciseData = this._getExerciseData(exerciseId);
        const kbData = this.knowledgeBase[exerciseId] || {};

        // Extract Code from Context (User Code or Example Code)
        // This ensures we analyze what the user is actually seeing/editing
        const codeFromContext = this._extractCodeFromContext(context);

        // 1. Intent Detection
        const intent = this._detectIntent(userMessage);

        // 2. Generate Response based on Intent + Data
        let responseText = "";

        switch (intent) {
            case 'ui_action':
                responseText = this._templateUIAction(userMessage);
                break;
            case 'concept':
                responseText = this._templateConcept(kbData, exerciseData, userMessage, codeFromContext);
                break;
            case 'explain_code':
                responseText = this._templateExplainCode(kbData, exerciseData, userMessage, codeFromContext);
                break;
            case 'instructions':
                responseText = this._templateInstructions(kbData, exerciseData, userMessage, codeFromContext);
                break;
            case 'summary':
                responseText = this._templateSummary(kbData, exerciseData, userMessage, codeFromContext);
                break;
            case 'step_by_step':
                responseText = this._templateStepByStep(kbData, exerciseData);
                break;
            case 'error':
                responseText = this._templateError(kbData, userMessage);
                break;
            case 'help':
                responseText = this._templateHelp(kbData, exerciseData, userMessage, codeFromContext);
                break;
            case 'course_info':
                responseText = "Este curso está diseñado para que aprendas Python paso a paso. A la izquierda tienes la teoría y las instrucciones. En el centro, el editor de código donde debes escribir tu solución. Y a la derecha (o abajo), verás el resultado al pulsar 'Ejecutar'. ¡No tengas miedo de romper cosas, es la mejor forma de aprender!";
                break;
            case 'motivation':
                responseText = this._templateMotivation(kbData);
                break;
            case 'identity':
                responseText = "Soy tu Profesor Lite del curso. Estoy aquí para explicarte cada ejercicio de forma clara y sencilla, sin inventar nada.";
                break;
            default:
                responseText = this._templateFallback(kbData, exerciseData, userMessage, codeFromContext);
                break;
        }

        // Simulate streaming for better UX
        if (callbacks.onToken) {
            const tokens = responseText.split(/(?=[ \n])/); // Split by words/newlines
            for (const token of tokens) {
                callbacks.onToken(token);
                await new Promise(r => setTimeout(r, 10)); // Tiny delay for typing effect
            }
        }

        return { text: responseText };
    }

    // --- Helper Methods ---

    _extractCodeFromContext(context) {
        // Try to find User Code first, then Example Code
        const userCodeMatch = context.match(/User Code:\n```python\n([\s\S]*?)\n```/);
        if (userCodeMatch) return userCodeMatch[1];

        const exampleCodeMatch = context.match(/Example Code:\n```python\n([\s\S]*?)\n```/);
        if (exampleCodeMatch) return exampleCodeMatch[1];

        return null;
    }

    _extractExerciseId(context) {
        // Context string format: "--- CURRENT LESSON (ID: 1) ---"
        const match = context.match(/CURRENT LESSON \(ID: (\d+)\)/);
        return match ? match[1] : "0";
    }

    _extractReferencedLessonId(context) {
        // Context string format: "<<<REFERENCED_LESSON>>>\nID: 5\n..."
        const match = context.match(/<<<REFERENCED_LESSON>>>[\s\S]*?ID: (\d+)/);
        return match ? match[1] : null;
    }

    _extractReferencedModule(context) {
        // Context string format: "<<<MODULE_SUMMARY>>>Summary Text<<<END_MODULE_SUMMARY>>>"
        const match = context.match(/<<<MODULE_SUMMARY>>>([\s\S]*?)<<<END_MODULE_SUMMARY>>>/);
        return match ? match[1] : null;
    }

    _getExerciseData(id) {
        // Flatten the exercises list to find the one with matching ID
        if (!this.exercises) return null;
        for (const module of this.exercises) {
            for (const lesson of module.lessons) {
                if (lesson.id == id) return lesson;
            }
        }
        return null;
    }

    _detectIntent(msg) {
        const m = msg.toLowerCase();

        // UI Actions (How to run/execute)
        if (m.match(/c[óo]mo (lo )?(ejecut|corr|inici)|bot[óo]n|play|run/)) return 'ui_action';

        // Course Info
        if (m.match(/c[óo]mo (funciona|uso) (el|este) curso|qu[ée] es esto/)) return 'course_info';

        // Concepts (What is X?) - HIGH PRIORITY
        if (m.match(/qu[ée] (es|son|significa|hace)|concept|teor[íi]a|definici[óo]n|para qu[ée] sirve/)) return 'concept';

        // Explanation - HIGH PRIORITY
        if (m.match(/expl[íi]ca|entien|funcionamiento|analiza/)) return 'explain_code';

        // Instructions / What to do
        if (m.match(/qu[ée] (debo|tengo que) hacer|c[óo]mo (se hace|lo uso|funciona)|instrucciones|pasos|tarea/)) return 'instructions';

        // Summary / Goal
        if (m.match(/resum[en]|objetivo|de qu[ée] trata/)) return 'summary';

        // Step by step (Explicit request)
        if (m.match(/paso a paso|detall/)) return 'step_by_step';

        // Errors
        if (m.match(/error|fall[ao]|problema|bug|no funciona/)) return 'error';

        // Motivation / General Help
        if (m.match(/motiv|consejo|ayuda|socorro|no s[ée]|estoy perdido|no entiendo/)) return 'help';

        // Identity
        if (m.match(/qui[ée]n eres|qu[ée] eres|tu nombre/)) return 'identity';

        return 'unknown';
    }

    // --- Templates ---

    _templateUIAction(msg) {
        if (msg.match(/ejecut|corr|play|run|inici/)) {
            return "Para ejecutar el código, busca el botón **▶ Ejecutar** (Play) situado en la parte superior derecha del editor (o abajo en móviles).";
        }
        return "Usa los botones de la interfaz para controlar el editor. El botón Play (▶) ejecuta tu código.";
    }

    _templateInstructions(kb, ex, msg, code) {
        // Check for specific terms first
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        if (kb.line_by_line) {
            return `Aquí tienes lo que debes hacer en este ejercicio:\n\n${kb.line_by_line}\n\n¡Inténtalo y dime si te atascas!`;
        }
        return `Para este ejercicio "${ex.title}", revisa los comentarios en el código. Suelen indicar los pasos a seguir.`;
    }

    _templateExplainCode(kb, ex, msg, code) {
        // Try to find specific terms in the message
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        let response = "";

        if (kb.explanation) {
            response += `**Función del Ejercicio:**\n${kb.explanation}\n\n`;
        } else if (kb.summary) {
            response += `**Función del Ejercicio:**\n${kb.summary}\n\n`;
        }

        if (kb.concepts) {
            response += `**Conceptos Clave:**\n${kb.concepts}\n\n`;
        }

        if (kb.line_by_line) {
            response += `**Desglose de Comandos:**\n${kb.line_by_line}\n\n`;
        }

        if (response) return response.trim();

        const title = ex ? ex.title : "Ejercicio desconocido";
        return `Este ejercicio trata sobre "${title}". Analiza el código de ejemplo, está diseñado para enseñarte este concepto. ¿Qué parte te confunde más?`;
    }

    _templateSummary(kb, ex, msg, code) {
        // Check for specific terms first
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        if (kb.summary) {
            return `En resumen: ${kb.summary}`;
        }
        const title = ex ? ex.title : "este tema";
        return `El objetivo principal es dominar: ${title}.`;
    }

    _templateStepByStep(kb, ex) {
        if (kb.line_by_line) {
            return `Vamos a verlo paso a paso:\n\n${kb.line_by_line}`;
        }
        return "No tengo un desglose paso a paso guardado, pero si lees el código línea por línea verás que sigue una secuencia lógica.";
    }

    _templateError(kb, msg) {
        // 1. Check known errors in KB
        if (kb.errors) {
            for (const [errName, errDesc] of Object.entries(kb.errors)) {
                if (msg.includes(errName) || msg.toLowerCase().includes(errName.toLowerCase())) {
                    return `💡 Ese error (${errName}) es común aquí. ${errDesc}`;
                }
            }
        }

        // 2. Check for Terminal/Console specific errors
        if (msg.match(/terminal|consola/) && msg.match(/error|fall|no funciona/)) {
            return `Si la terminal te da error, es posible que este ejercicio requiera un entorno más completo. **Intenta realizarlo en tu IDS (Entorno de Desarrollo Local)** para asegurar que todo funcione correctamente.`;
        }

        // 3. General advice if no specific error match
        return `Entiendo que tienes problemas. Si te sale un mensaje de error en rojo, cópialo y pégalo aquí para que pueda decirte exactamente qué pasa.\n\nSi el código no hace nada, asegúrate de haber pulsado el botón "▶ Ejecutar".\n\n(Nota: Si el error persiste en la terminal, prueba a ejecutarlo en tu IDS local).`;
    }

    _templateHelp(kb, ex, msg, code) {
        // Check for specific terms first
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        let response = "No te preocupes, es normal atascarse a veces. ";
        if (kb.summary) {
            response += `Recuerda que el objetivo es: ${kb.summary}\n\n`;
        }
        if (kb.line_by_line) {
            response += `Intenta seguir estos pasos:\n${kb.line_by_line}`;
        } else {
            response += "Revisa las instrucciones en el panel izquierdo y el código de ejemplo.";
        }
        return response;
    }

    _templateConcept(kb, ex, msg, code) {
        // Try to find specific terms in the message
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        if (kb.concepts) {
            return `Conceptos clave: ${kb.concepts}`;
        }
        return "Este ejercicio se centra en conceptos fundamentales de Python. ¿Hay alguna palabra específica que no entiendas?";
    }

    _templateMotivation(kb) {
        return "¡Vas muy bien! La programación es una carrera de fondo. Cada error es una oportunidad para aprender algo nuevo. ¡Sigue así!";
    }

    _templateFallback(kb, ex, msg, code) {
        // Try to find specific terms in the message even in fallback
        const termExplanation = this._findTermInKB(msg, kb, ex, code);
        if (termExplanation) return termExplanation;

        // More conversational fallback
        const title = ex ? ex.title : "el ejercicio actual";
        let info = kb.summary ? `Sobre "${title}": ${kb.summary}` : `Estoy aquí para ayudarte con "${title}".`;

        return `${info}\n\nNo estoy seguro de haber entendido tu última pregunta. ¿Podrías reformularla? Puedes preguntarme "qué debo hacer", "explícame el código" o pegarme un error.`;
    }

    // --- Smart Search ---

    _findTermInKB(msg, currentKb, currentEx, codeFromContext) {
        // Dynamic Keyword Extraction
        const keywords = this._extractKeywords(msg);

        // 1. First Pass: Check for Variables in Current Code (Highest Priority)
        // We check ALL keywords against the code first to ensure specific variables 
        // (e.g., "nombre") take precedence over generic terms (e.g., "variable").

        // Use code from context if available, otherwise fallback to example_code
        const codeToScan = codeFromContext || (currentEx ? currentEx.example_code : null);

        if (codeToScan) {
            for (const term of keywords) {
                // Look for "term = ..." assignments
                const varRegex = new RegExp(`^\\s*${term}\\s*=.*?(?:#\\s*(.*))?$`, 'im');
                const match = codeToScan.match(varRegex);

                if (match) {
                    const comment = match[1];
                    if (comment) {
                        return `💡 **Variable \`${term}\`:**\nSe usa para: ${comment.trim()}`;
                    } else {
                        return `💡 **Variable \`${term}\`:**\nEs una variable definida en el código de este ejercicio. Revisa dónde se asigna su valor.`;
                    }
                }
            }
        }

        // 2. Second Pass: Check Glossary and Knowledge Base
        for (const term of keywords) {
            // Check if term is present as a whole word (regex boundary)
            const regex = new RegExp(`\\b${term}\\b`, 'i');

            // 0. Check Glossary (Highest Priority for Definitions)
            // We check if the term matches a key in the glossary (case-insensitive)
            if (this.glossary) {
                const glossaryKey = Object.keys(this.glossary).find(k => k.toLowerCase() === term);
                if (glossaryKey) {
                    return `💡 **Definición de \`${glossaryKey}\`:**\n${this.glossary[glossaryKey]}`;
                }
            }

            // 1. Check current exercise first (Priority)
            if (currentKb.explanation && regex.test(currentKb.explanation)) {
                return `**Sobre "${term}" en este ejercicio:**\n${currentKb.explanation}`;
            }
            if (currentKb.concepts && regex.test(currentKb.concepts)) {
                return `**Concepto "${term}":** ${currentKb.concepts}`;
            }

            // 2. Check GLOBAL KB (Search other exercises)
            for (const [id, data] of Object.entries(this.knowledgeBase)) {
                // Search in explanation, summary, and concepts
                const content = (data.explanation || "") + (data.summary || "") + (data.concepts || "");
                if (regex.test(content)) {
                    // Found a mention in another exercise
                    // We return a snippet of the explanation or summary
                    const snippet = data.explanation || data.summary || "Concepto avanzado.";
                    // CLEANER RESPONSE FORMAT
                    return `💡 **Concepto: ${term}** (Visto en Ejercicio ${id})\n\n"${snippet}"`;
                }
            }

            // 3. Hardcoded fallback for very common terms if not found in KB (Safety net)
            if (term === 'print') return "`print()` es una función que sirve para mostrar texto o números en la pantalla (consola).";
            if (term === 'input') return "`input()` sirve para pedirle al usuario que escriba algo con el teclado.";
            if (term === 'variable') return "Una variable es como una caja donde guardas datos (números, texto) para usarlos después.";
            if (term === 'entero' || term === 'int') return "Un **entero** (`int`) es un número sin decimales (ej: 5, -10, 0).";
            if (term === 'cadena' || term === 'string' || term === 'str' || term === 'texto') return "Una **cadena** (`str`) es texto encerrado entre comillas (ej: \"Hola\").";
            if (term === 'booleano' || term === 'bool') return "Un **booleano** (`bool`) solo puede ser Verdadero (`True`) o Falso (`False`).";
        }
        return null;
    }
    async _streamResponse(text, callbacks) {
        if (callbacks.onToken) {
            const tokens = text.split(/(?=[ \n])/); // Split by words/newlines
            for (const token of tokens) {
                callbacks.onToken(token);
                await new Promise(r => setTimeout(r, 20)); // Slower typing for better UX
            }
        }
    }


    _extractKeywords(msg) {
        // 1. Tokenize (split by non-word chars, keep Spanish accents)
        // We want to keep technical terms (often English) and Spanish words
        const words = msg.toLowerCase().split(/[^a-záéíóúñ0-9_]+/);

        // 2. Filter Stopwords (Spanish + Common Chat)
        const stopwords = new Set([
            "que", "qué", "como", "cómo", "para", "sirve", "hace", "hacer", "el", "la", "los", "las",
            "un", "una", "unos", "unas", "de", "del", "en", "con", "por", "y", "o", "u",
            "es", "son", "esta", "está", "este", "esto", "ese", "eso", "esa", "mi", "tu", "su",
            "yo", "tú", "él", "ella", "nosotros", "vosotros", "ellos", "ellas",
            "me", "te", "se", "lo", "la", "le", "nos", "os", "les",
            "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante",
            "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según",
            "sin", "so", "sobre", "tras", "versus", "via",
            "hola", "adios", "gracias", "por favor", "ayuda", "explica", "explicame", "dime",
            "ejercicio", "codigo", "funciona", "uso", "usar", "ejecutar", "correr",
            "debo", "tengo", "puedo", "quiero", "necesito", "voy", "vamos", "ver", "mirar"
        ]);

        const keywords = [];
        for (const w of words) {
            if (w.length > 1 && !stopwords.has(w)) {
                keywords.push(w);
            }
        }
        return keywords;
    }
}
