# 🛡️ PythonTutor-Web: Aprende Ciberseguridad con Python

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)
![Platform](https://img.shields.io/badge/platform-web-orange.svg)

**Bienvenido a PythonTutor-Web**, la plataforma definitiva para aprender Python orientado a ciberseguridad directamente desde tu navegador. Sin instalaciones complejas, sin servidores, y con la ayuda de un potente Tutor de Inteligencia Artificial.

### 🔗 [¡Pruébalo ahora en vivo!](https://python-tutor-es.netlify.app/)
**Acceso directo:** https://python-tutor-es.netlify.app/

---

## 📖 Descripción General

**PythonTutor-Web** es un entorno de desarrollo y aprendizaje interactivo diseñado para llevarte desde "Hola Mundo" hasta la creación de scripts de seguridad avanzados.

### ¿Por qué es ideal para ti?
*   **🚀 Todo en el navegador:** No necesitas instalar Python ni configurar entornos virtuales. Entra y empieza a programar.
*   **🧠 Aprendizaje Guiado:** Un currículo estructurado paso a paso con teoría y práctica integrada.
*   **🤖 Tutor IA Personal:** Un asistente inteligente siempre disponible para explicarte código, corregir errores y resolver dudas.
*   **🔒 Privacidad Total:** Todo se ejecuta en tu dispositivo. Tu código y tus claves nunca salen de tu navegador.

---

## ✨ Características Principales

### A. Editor de Código Real (Pyodide)
Olvídate de simulaciones. PythonTutor-Web utiliza **Pyodide** (Python compilado a WebAssembly) para ejecutar código Python real directamente en tu navegador.
*   **Rápido y Seguro:** La ejecución es local y aislada (sandbox).
*   **Librerías Estándar:** Acceso a la mayoría de las librerías estándar de Python.
*   **Multiplataforma:** Funciona en Windows, Mac, Linux, Tablets y Móviles.

### B. Sistema de Lecciones Interactivas
El aprendizaje se organiza en **Módulos** temáticos (Fundamentos, Estructuras de Datos, Ciberseguridad, etc.).
*   **Progreso Visual:** Marca tus lecciones completadas.
*   **Teoría y Práctica:** Cada lección incluye una explicación clara y un ejercicio práctico.
*   **Feedback Inmediato:** Ejecuta tu código y ve el resultado al instante en la terminal integrada.

---

## 🤖 Configuración del Chat de IA

El sistema elige automáticamente el mejor modo para tu dispositivo, pero puedes configurarlo manualmente:

### 1. ☁️ Modo API (⭐ Recomendado)
**La mejor experiencia posible.**
Si quieres respuestas rápidas, precisas y detalladas (como GPT-4 o Claude), esta es la opción ideal.
*   **Cómo funciona:** Conectas tu propia API Key (OpenAI, Groq, DeepSeek).
*   **Privacidad:** Tu clave se guarda **encriptada en tu navegador**. Nunca se envía a nosotros.
*   **Costo:** Depende de tu proveedor (Groq y DeepSeek son muy baratos/gratis).

### 2. 🚀 Modo Local (WebGPU / Lite)
**Ideal para privacidad total o uso offline.**
*   **WebGPU:** Si tienes tarjeta gráfica, usa modelos potentes (Qwen 2.5) en tu navegador.
*   **Lite (CPU):** Funciona en cualquier CPU, pero es más lento y básico.

### 3. 📂 Modo Local GGUF (Avanzado)
**Para usuarios expertos.**
Carga tus propios modelos `.gguf` (Llama 3, Mistral, etc.) desde tu disco duro.
*   **Nota:** Requiere un dispositivo con buena memoria RAM. Recomendamos modelos < 500MB.

---

## 🚀 Guía de Despliegue (Netlify / GitHub Pages)

Este proyecto es 100% estático, lo que significa que puedes alojarlo gratis en cualquier CDN.

### Pasos para Desplegar en Netlify

1.  **Preparar el Repositorio:**
    *   Asegúrate de que tu repositorio en GitHub/GitLab está limpio.
    *   **NO subas** archivos de modelos grandes (`.gguf`) ni carpetas `venv`.

2.  **Crear Sitio en Netlify:**
    *   Entra en [Netlify](https://www.netlify.com/) > **"Add new site"** > **"Import an existing project"**.
    *   Conecta tu repositorio.

3.  **Configuración de Build:**
    *   **Base directory:** `/` (raíz)
    *   **Build command:** `(dejar vacío)` (No hay compilación)
    *   **Publish directory:** `public`

4.  **Desplegar:**
    *   Haz clic en **"Deploy site"**. ¡Listo!

---

## 💻 Ejecución Local (Para Desarrolladores)

Si deseas modificar el proyecto o ejecutarlo offline en tu máquina:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/python-tutor-web.git
    cd python-tutor-web
    ```

2.  **Estructura de Carpetas:**
    ```text
    /
    ├── public/             # Archivos estáticos (sitio web final)
    │   ├── index.html      # Punto de entrada
    │   ├── static/
    │   │   ├── css/        # Estilos
    │   │   ├── js/         # Lógica (app.js, ai_chat.js, llm_local_adapter.js)
    │   │   └── exercises_v2.json # Contenido del curso
    ├── scripts/            # Scripts de utilidad (generadores, conversores)
    ├── tests/              # Tests de lógica
    ├── src/                # Código fuente Python (herramientas)
    └── README.md           # Esta documentación
    ```

3.  **Iniciar Servidor:**
    Solo necesitas un servidor HTTP simple para servir la carpeta `public`.
    *   Con Python: `python3 -m http.server 8000` (luego ve a `/public`)
    *   Con Node: `npx serve public`

4.  **Abrir:** Navega a `http://localhost:8000`.

> [!WARNING]
> **Nota sobre el Audio (TTS):**
> La función de lectura de voz (TTS) depende de las voces instaladas en tu sistema operativo o de la conexión a internet (Google TTS Fallback).
> *   En entornos **Linux/Local** sin voces configuradas, es posible que el audio no funcione correctamente o suene robótico.
> *   Si ves errores como `TTS: Timeout waiting for voices` o `synthesis-failed`, asegúrate de tener paquetes de voz instalados (ej: `speech-dispatcher` en Linux) o conexión a internet activa.

---

## 🔒 Seguridad y Privacidad

Nos tomamos tu seguridad muy en serio:

*   **Sin Backend:** No hay base de datos ni servidor que almacene tu información.
*   **API Keys Locales:** Si usas el Modo API, tu clave se guarda encriptada en el almacenamiento local de tu navegador. Si borras la caché, se borra la clave.
*   **Entorno Seguro:** El código Python se ejecuta en una sandbox (Pyodide) que no tiene acceso directo a tu sistema de archivos local.
*   **Apto para Menores:** Al no haber interacción con otros usuarios ni recopilación de datos, es un entorno seguro para el aprendizaje.

---

## 🏆 Créditos y Autoría

**Creador y Desarrollador Principal:**
### 👨‍💻 Carlos Dominguez

**Proyecto:** PythonTutor-Web (Educational Open Source)

Agradecimientos especiales a:
*   Proyecto [Pyodide](https://pyodide.org/) por hacer posible Python en la web.
*   [Transformers.js](https://huggingface.co/docs/transformers.js) y [Wllama](https://github.com/wllama/wllama) por la IA local.
*   Comunidad de Código Abierto.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Eres libre de usarlo, modificarlo y compartirlo con fines educativos.

*¡Feliz Python Ético!* 🕵️‍♂️
