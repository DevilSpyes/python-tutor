# 🛡️ PythonTutor-Web: Aprende Ciberseguridad con Python

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)
![Platform](https://img.shields.io/badge/platform-web-orange.svg)

**Bienvenido a PythonTutor-Web**, la plataforma definitiva para aprender Python orientado a ciberseguridad directamente desde tu navegador. Sin instalaciones complejas, sin servidores, y con la ayuda de un potente Tutor de Inteligencia Artificial.

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

## 🤖 Configuración del Chat de IA (Sistema Unificado)

El sistema elige automáticamente el mejor modo para tu dispositivo:

### 🚀 Modo A: WebGPU (Alto Rendimiento)
*   **Activación:** Automática si tu navegador soporta WebGPU (Chrome/Edge + GPU).
*   **Modelo:** Qwen2.5-0.5B (Ejecutado en GPU).
*   **Rendimiento:** Rápido y fluido.

### 🐌 Modo B: Lite (CPU / Universal)
*   **Activación:** Automática si no tienes WebGPU (Móviles antiguos, Firefox, Safari).
*   **Modelo:** Qwen2.5-0.5B (Cuantizado Int8).
*   **Rendimiento:** Más lento, pero funciona en cualquier lugar.

### ☁️ Modo API (Opcional)
*   Si prefieres usar modelos más potentes (GPT-4, Llama 3), puedes configurar tu **API Key** en los ajustes.

---

## 📂 Gestión de Modelos (Offline)

Por defecto, el sistema descarga los modelos de HuggingFace la primera vez.
Si quieres instalarlos manualmente para uso offline:

1.  Ve a `public/static/models/`.
2.  Lee el archivo `DOWNLOAD_MODELS.md`.
3.  Coloca los archivos `.onnx` en las carpetas correspondientes (`qwen-webgpu` o `lite`).

#### ☁️ Opción 2: IA vía API (Tu Clave)
*   **Tecnología:** Conexión directa a proveedores como OpenAI, Groq o DeepSeek.
*   **Cómo funciona:** Introduces tu propia API Key en la configuración.
*   **Seguridad:** La clave se guarda **exclusivamente en el localStorage** de tu navegador. Nunca se envía a nuestros servidores (porque no tenemos).

---

## � Guía Rápida de Uso

1.  **Accede a la Plataforma:** Abre la URL del proyecto (ej. en Netlify).
2.  **Selecciona un Módulo:** Empieza por el Módulo 00 si eres principiante.
3.  **Lee la Lección:** La teoría aparecerá en el panel central.
4.  **Escribe tu Código:** Usa el editor para resolver el ejercicio propuesto.
5.  **Ejecuta:** Pulsa el botón `▶ Ejecutar` y observa la terminal.
6.  **¿Dudas? Pregunta a la IA:**
    *   Abre el panel derecho.
    *   Configura tu modo (Local o API).
    *   Pregunta: *"¿Por qué falla mi bucle?"* o *"Explícame este código"*.

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
    │   │   ├── css/        # Estilos (style.css, ai_chat.css)
    │   │   ├── js/         # Lógica (app.js, ai_chat.js, etc.)
    │   │   └── lessons/    # Contenido del curso (JSON/Markdown)
    ├── README.md           # Esta documentación
    └── ...
    ```

3.  **Iniciar Servidor:**
    Como es un proyecto estático, solo necesitas un servidor HTTP simple.
    *   Con Python: `python3 -m http.server 8000`
    *   Con Node: `npx serve public`

4.  **Abrir:** Navega a `http://localhost:8000` (o la carpeta `public` si usas el servidor de Python en la raíz, ajusta la ruta).

---

## ☁️ Despliegue en Netlify

Este proyecto está optimizado para **Netlify** y otros hostings estáticos.

1.  **Nuevo Sitio:** En Netlify, selecciona "Import from Git".
2.  **Configuración de Build:**
    *   **Base directory:** `/` (raíz)
    *   **Build command:** `(dejar vacío)`
    *   **Publish directory:** `public`
3.  **Desplegar:** Haz clic en "Deploy Site".

> **Nota:** No se requieren funciones serverless ni configuraciones extra. El sitio es 100% Client-Side.

---

## 🔒 Seguridad y Privacidad

Nos tomamos tu seguridad muy en serio:

*   **Sin Backend:** No hay base de datos ni servidor que almacene tu información.
*   **API Keys Locales:** Si usas el Modo API, tu clave se guarda encriptada en el almacenamiento local de tu navegador. Si borras la caché, se borra la clave.
*   **Entorno Seguro:** El código Python se ejecuta en una sandbox (Pyodide) que no tiene acceso directo a tu sistema de archivos local.
*   **Apto para Menores:** Al no haber interacción con otros usuarios ni recopilación de datos, es un entorno seguro para el aprendizaje.

---

## 🤝 Créditos

**Autor:** [Tu Nombre / Alias]
**Proyecto:** PythonTutor-Web (Educational Open Source)

Agradecimientos especiales a:
*   Proyecto [Pyodide](https://pyodide.org/) por hacer posible Python en la web.
*   [WebLLM](https://webllm.mlc.ai/) por la tecnología de IA local.
*   Comunidad de Código Abierto.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Eres libre de usarlo, modificarlo y compartirlo con fines educativos.

---

*¡Feliz Hacking Ético!* 🕵️‍♂️�
