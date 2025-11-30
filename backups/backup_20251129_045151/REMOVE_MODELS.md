# Guía de Gestión de Modelos (REMOVE_MODELS)

Este repositorio ha sido optimizado para despliegue estático en **Netlify**.
Por tanto, **NO** debe contener archivos binarios grandes (modelos de IA) como `.gguf`, `.bin` o `.onnx` que superen los 50MB.

## 1. Qué eliminar
Busca y elimina (o mueve a una carpeta fuera del proyecto) cualquier archivo con estas extensiones:
*   `*.gguf`
*   `*.bin`
*   `*.pth`

## 2. Cómo usar modelos locales
Si deseas usar un modelo local, tienes dos opciones:

### Opción A: WebLLM (Recomendado)
La aplicación ya integra **WebLLM**.
1.  Ve a Ajustes > Chat.
2.  Selecciona "Modo Local".
3.  El navegador descargará y cacheará el modelo automáticamente desde HuggingFace CDN. **No necesitas subir nada.**

### Opción B: Servidor Propio
Si tienes un modelo personalizado (`.gguf`) y quieres usarlo:
1.  Alójalo en un servidor externo (VPS, S3, o tu propio PC con `python -m http.server`).
2.  Asegúrate de habilitar **CORS**.
3.  En la web, ve a Ajustes > Chat > "Usar Modelo Remoto".
4.  Pega la URL de tu servidor.
