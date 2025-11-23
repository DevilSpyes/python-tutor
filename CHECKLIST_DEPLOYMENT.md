# Checklist de Despliegue

Antes de publicar, verifica los siguientes puntos:

## ✅ Repositorio
- [ ] **Limpieza:** No hay archivos `.gguf`, `.bin` o `.onnx` grandes en el historial.
- [ ] **.gitignore:** Contiene reglas para excluir modelos y entornos virtuales.
- [ ] **Secretos:** No hay API keys hardcodeadas en `app.js` o `index.html`.

## ✅ Frontend (UI)
- [ ] **Carga:** La página carga sin errores de consola (`F12`).
- [ ] **Ajustes:** El botón de ajustes abre el modal de configuración.
- [ ] **Persistencia:** Al recargar la página, la API Key guardada se mantiene.
- [ ] **Modo API:** El chat funciona correctamente con una API Key válida (Groq/OpenAI).
- [ ] **Modo Local:** (Opcional) WebLLM inicia la descarga si se selecciona.

## ✅ Configuración Netlify
- [ ] **Publish Directory:** Está configurado a `public/`.
- [ ] **Build Command:** Está vacío (o es el correcto si añades bundlers).
- [ ] **HTTPS:** El sitio carga con candado seguro (Netlify lo activa por defecto).

## 🚨 Solución de Problemas Comunes
*   **Error 404 en recursos:** Verifica que las rutas en `index.html` son relativas (ej. `./static/...`) o absolutas correctas.
*   **CORS Error (Modelo Remoto):** Tu servidor de modelos debe permitir el origen de Netlify (`Access-Control-Allow-Origin`).
*   **"Address already in use" (Local):** Usa `dev_server.sh` para matar procesos antiguos.
