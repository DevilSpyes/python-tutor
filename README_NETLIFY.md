# Despliegue en Netlify (Sitio Estático)

Este proyecto ha sido configurado para funcionar como un sitio web 100% estático, lo que lo hace ideal para desplegar en **Netlify**, **GitHub Pages** o **Vercel** sin necesidad de servidores backend complejos.

## 🚀 Pasos para Desplegar

### 1. Preparar el Repositorio
Asegúrate de que tu repositorio en GitHub/GitLab está limpio y actualizado.
*   **NO subas** archivos de modelos grandes (`.gguf`).
*   Verifica que `.gitignore` excluye `venv/` y `__pycache__/`.

### 2. Crear Sitio en Netlify
1.  Entra en [Netlify](https://www.netlify.com/) y haz clic en **"Add new site"** > **"Import an existing project"**.
2.  Conecta con tu proveedor de Git (GitHub, GitLab, etc.).
3.  Selecciona el repositorio `python_tutor`.

### 3. Configuración de Build
Netlify detectará la configuración automáticamente, pero asegúrate de usar estos valores:

*   **Base directory:** `/` (raíz)
*   **Build command:** `(dejar vacío)` (No hay paso de compilación)
*   **Publish directory:** `public`

> **Nota:** Si usas un generador estático en el futuro, ajusta el comando de build. Por ahora, es HTML/JS puro.

### 4. Desplegar
Haz clic en **"Deploy site"**. En unos segundos, tu sitio estará online con una URL tipo `https://tu-sitio.netlify.app`.

---

## ⚙️ Configuración del Chat (Post-Despliegue)

Una vez el sitio esté online, la funcionalidad de IA (Chat) requerirá configuración por parte del usuario final, ya que no hay servidor backend.

### Opción A: Usar API Key (Recomendado)
1.  Abre tu sitio web desplegado.
2.  Haz clic en el icono de **Ajustes (⚙️)** en la barra lateral o en el panel de IA.
3.  Selecciona **"Usar API Key"**.
4.  Elige tu proveedor (OpenAI, Groq, DeepSeek) e introduce tu **API Key**.
    *   *La clave se guarda de forma segura en el almacenamiento local de tu navegador (localStorage). Nunca se envía a ningún servidor que no sea el proveedor oficial.*

### Opción B: IA Local (WebGPU)
1.  En Ajustes, selecciona **"IA Local"**.
2.  El navegador descargará un modelo ligero (~300MB) y lo ejecutará usando tu tarjeta gráfica.
    *   *Requiere un navegador moderno (Chrome/Edge) y una GPU compatible.*

### Opción C: Modelo Remoto (Avanzado)
Si prefieres alojar tu propio modelo (ej. con `ollama` o `llama.cpp` en un servidor propio):
1.  Asegúrate de que tu servidor tiene **CORS habilitado** para permitir peticiones desde tu dominio de Netlify.
2.  En Ajustes, selecciona **"Modelo Remoto"**.
3.  Introduce la URL completa de tu endpoint (ej: `https://mi-servidor.com/v1/chat/completions`).

---

## 🛡️ Seguridad
*   **API Keys:** Nunca subas tus API keys al repositorio de código.
*   **Privacidad:** Todo el historial de chat y las configuraciones residen en el navegador del usuario.
