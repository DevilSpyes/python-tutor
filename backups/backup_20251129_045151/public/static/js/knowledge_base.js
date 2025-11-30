/**
 * knowledge_base.js
 * Generates a massive database of 1000+ questions/answers for the Semantic Search Engine.
 */

import { STATIC_QA_DATA } from "./knowledge_base_data.js";

export class KnowledgeBase {
    constructor() {
        this.topics = [
            // Basics
            { id: "print", name: "print", desc: "Muestra texto en consola", code: "print('Hola')" },
            { id: "input", name: "input", desc: "Pide datos al usuario", code: "nombre = input('¿Nombre?')" },
            { id: "variable", name: "variables", desc: "Guardan datos", code: "x = 10" },
            { id: "comment", name: "comentarios", desc: "Notas en el código (#)", code: "# Esto es un comentario" },

            // Types
            { id: "int", name: "enteros (int)", desc: "Números sin decimales", code: "x = 5" },
            { id: "float", name: "flotantes (float)", desc: "Números con decimales", code: "pi = 3.14" },
            { id: "str", name: "cadenas (string)", desc: "Texto entre comillas", code: "s = 'Hola'" },
            { id: "bool", name: "booleanos", desc: "True o False", code: "es_valido = True" },

            // Structures
            { id: "list", name: "listas", desc: "Colección ordenada modificable", code: "lista = [1, 2, 3]" },
            { id: "tuple", name: "tuplas", desc: "Colección ordenada inmutable", code: "tupla = (1, 2)" },
            { id: "dict", name: "diccionarios", desc: "Pares clave-valor", code: "d = {'a': 1}" },
            { id: "set", name: "conjuntos", desc: "Colección sin duplicados", code: "s = {1, 2}" },

            // Control
            { id: "if", name: "condicional if", desc: "Ejecuta si es verdad", code: "if x > 0: print('Positivo')" },
            { id: "else", name: "else", desc: "Si no se cumple el if", code: "else: print('Negativo')" },
            { id: "for", name: "bucle for", desc: "Itera sobre una secuencia", code: "for i in range(5): print(i)" },
            { id: "while", name: "bucle while", desc: "Repite mientras sea verdad", code: "while x > 0: x -= 1" },
            { id: "break", name: "break", desc: "Rompe el bucle", code: "break" },
            { id: "continue", name: "continue", desc: "Salta a la siguiente iteración", code: "continue" },

            // Functions
            { id: "def", name: "funciones", desc: "Bloques de código reutilizables", code: "def saludar(): print('Hola')" },
            { id: "return", name: "return", desc: "Devuelve un valor", code: "return x + 1" },
            { id: "lambda", name: "lambda", desc: "Función anónima corta", code: "doble = lambda x: x * 2" },

            // Advanced
            { id: "class", name: "clases", desc: "Plantillas para objetos", code: "class Perro: pass" },
            { id: "import", name: "importar módulos", desc: "Usar código externo", code: "import math" },
            { id: "try", name: "excepciones try/except", desc: "Manejo de errores", code: "try: x/0\nexcept: print('Error')" },
            { id: "file", name: "archivos open", desc: "Leer/Escribir archivos", code: "with open('f.txt') as f: print(f.read())" },

            // Errors
            { id: "syntax_error", name: "SyntaxError", desc: "Error de escritura (falta :, (), etc)", code: "# Revisa paréntesis y dos puntos" },
            { id: "indentation_error", name: "IndentationError", desc: "Error de espacios/tabulaciones", code: "# Alinea bien el código" },
            { id: "name_error", name: "NameError", desc: "Variable no definida", code: "# Define la variable antes de usarla" },
            { id: "type_error", name: "TypeError", desc: "Operación con tipos incompatibles", code: "str(5) + 'hola'" },
            { id: "index_error", name: "IndexError", desc: "Índice fuera de rango", code: "# Revisa el tamaño de la lista" }
        ];

        this.templates = [
            "¿Qué es {x}?",
            "Explícame {x}",
            "Cómo funciona {x}",
            "Ejemplo de {x}",
            "Ayuda con {x}",
            "No entiendo {x}",
            "Error en {x}",
            "Para qué sirve {x}",
            "Cómo usar {x} en Python",
            "Definición de {x}",
            "Diferencia de {x}",
            "Problema con {x}",
            "Sintaxis de {x}",
            "Tutorial de {x}",
            "Guía rápida {x}",
            "Qué hace {x}",
            "Cómo arreglo {x}",
            "Me sale {x}"
        ];
    }

    getStaticQA() {
        return STATIC_QA_DATA;
    }

    generate() {
        const knowledge = [];

        this.topics.forEach(topic => {
            this.templates.forEach(template => {
                const question = template.replace("{x}", topic.name);

                // Optimized Template Answer
                const answer = `### 🚀 ${topic.name.toUpperCase()}
**Explicación:** ${topic.desc}

**Ejemplo:**
\`\`\`python
${topic.code}
\`\`\`

*(Respuesta Instantánea)*`;

                knowledge.push({
                    q: question,
                    a: answer,
                    topic: topic.id
                });
            });
        });

        // Add Definitive QA Pack (High Priority Static Intents)
        STATIC_QA_DATA.forEach(item => {
            knowledge.push({
                q: item.q,
                a: item.a,
                topic: "static_qa",
                type: "static" // Critical for Semantic Search to detect exact matches
            });
        });

        return knowledge;
    }
}
