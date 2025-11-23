from data.exercises import Module, Lesson

MODULE = Module(
    id=0,
    title="Módulo 00: Bienvenida y Guía",
    lessons=[
        Lesson(
            id=1,
            title="Guía de Inicio y Créditos",
            content="""# 👋 Bienvenido al Curso de Python orientado a Ciberseguridad

¡Hola! Soy **Carlos Domínguez**, y te doy la bienvenida a este proyecto formativo diseñado para acompañarte desde **cero absoluto** hasta un nivel **intermedio–avanzado** en Python.

Este curso tiene un enfoque aplicado a:
*   🤖 Automatización
*   🔒 Seguridad Informática
*   📊 Análisis Técnico

---

## 🎯 ¿Qué vas a encontrar aquí?

Este proyecto está pensado para que **aprendas haciendo**, avanzando paso a paso con explicaciones detalladas y ejercicios prácticos.

**Al finalizar, serás capaz de:**

*   ✅ Entender y dominar la sintaxis base de Python.
*   ✅ Automatizar tareas repetitivas o complejas.
*   ✅ Analizar código y crear herramientas funcionales.
*   ✅ Aplicar Python en **Ciberseguridad** (escáneres, auditoría, scripts, etc.).

---

## 📌 Filosofía del curso

> *"Este curso es de carácter libre y sin ánimo de lucro. Mi intención es compartir conocimiento y ayudarte a construir una base sólida."*

Aquí **tú eres el protagonista**: tu ritmo, tu curiosidad y tu práctica son lo que te harán mejorar.

---

## 🛠️ Recomendaciones importantes

### 1. Usa un IDE profesional
Aunque cuentas con un editor integrado, te recomiendo trabajar también con herramientas reales para ganar experiencia:
*   **Visual Studio Code**
*   **PyCharm**
*   **Thonny** (ideal para principiantes)

### 2. Experimenta sin miedo
No te limites a copiar y pegar. **Modifica, rompe y arregla** el código. Así se aprende de verdad.

### 3. Sé constante
Dedícale al menos **20 minutos al día**. La programación no se memoriza, **se practica**.

---

## 📚 Plan de estudios

*   **🔹 Módulo 01:** Sintaxis básica, variables y lógica fundamental.
*   **🔹 Módulo 02:** Estructuras de datos, funciones y control de flujo.
*   **🔹 Módulo 03:** Algoritmos y resolución de problemas.
*   **🔹 Módulo 04:** Automatización de tareas y scripts útiles.
*   **🔹 Módulo 05:** Herramientas de ciberseguridad y criptografía.
*   **🔹 Módulo 06:** Proyectos completos (bots, herramientas).
*   **🔹 Módulo 07:** Prueba y certificación final.

---

## 🚀 ¡Comencemos!

Siéntete libre de explorar, practicar y avanzar a tu ritmo. Este camino lo recorres tú, y yo estaré aquí para guiarte.

**¡Disfruta el viaje y bienvenido al mundo de Python!**""",
            example_code="# Bienvenido al curso.\n# Este es un espacio para aprender y experimentar.\n\nprint('¡Hola, mundo! Estoy listo para aprender Python.')",
            exercise_prompt="Lee la guía y ejecuta el código de prueba.",
            validator=lambda code: (True, "¡Bienvenido a bordo!"),
            hint="Simplemente haz clic en Ejecutar.",
            type="informational"
        ),
    ]
)
