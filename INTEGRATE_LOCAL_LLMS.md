# Integración de Modelos LLM Locales (Tiny AI)

Este documento describe cómo funciona la integración de IA Local en el proyecto Python Tutor, permitiendo ejecutar modelos de lenguaje directamente en el navegador del usuario sin necesidad de servidores externos ni API keys.

## 1. Arquitectura

El sistema utiliza **Transformers.js** para ejecutar modelos cuantizados (ONNX) en el navegador.

- **Runtime**: `static/js/llm_runtime_loader.js` (Lazy loading de la librería).
- **Adapter**: `static/js/llm_local_adapter.js` (Interfaz unificada para WebGPU/WASM).
- **Modelo por defecto**: `Xenova/Qwen1.5-0.5B-Chat` (~300MB). Es un modelo "Tiny" optimizado para instrucciones.

### Flujo de Carga
1. El usuario selecciona "Modo Local" (o se detecta automáticamente).
2. Se descarga el runtime solo cuando es necesario.
3. Se descarga el modelo desde Hugging Face Hub (caché persistente en navegador).
4. Si el navegador soporta **WebGPU**, se usa para aceleración gráfica (rápido).
5. Si no, se hace fallback a **WASM (CPU)** (más lento, pero universal).

## 2. Cómo Integrar Nuevos Modelos

Para cambiar el modelo por defecto o añadir opciones, edita `static/js/llm_local_adapter.js`:

```javascript
this.modelId = "Xenova/Qwen1.5-0.5B-Chat"; 
// Opciones probadas:
// - "Xenova/TinyLlama-1.1B-Chat-v1.0" (Más grande, mejor calidad)
// - "Xenova/gpt2" (Muy pequeño, mala calidad para chat)
```

### Hosting Propio (Offline / Intranet)
Si necesitas que el modelo funcione sin internet tras la primera carga o desde una red interna:

1. Descarga los archivos ONNX del modelo (carpeta `onnx` y `config.json`, `tokenizer.json`, etc.).
2. Colócalos en una carpeta pública, ej: `/public/models/my-model/`.
3. En `llm_local_adapter.js`, cambia `this.modelId` por la ruta relativa o absoluta.
4. Asegúrate de que `env.allowLocalModels = true` en el loader.

## 3. Pruebas Locales

Para verificar el funcionamiento sin la interfaz completa, usa el archivo `test_local_llm.html` (ver sección de pruebas).

### Comandos de Verificación
Abre la consola del navegador y ejecuta:

```javascript
// Verificar soporte WebGPU
navigator.gpu.requestAdapter().then(a => console.log(a ? "GPU OK" : "No GPU"));
```

## 4. Rendimiento Esperado

| Dispositivo | Backend | Carga Inicial | Velocidad (Tokens/s) |
|-------------|---------|---------------|----------------------|
| PC Gaming (RTX) | WebGPU | < 5s | > 50 t/s |
| Laptop (M1/M2) | WebGPU | < 5s | > 30 t/s |
| Laptop (Intel) | WASM (CPU)| ~10s | ~2-5 t/s |
| Móvil Gama Alta | WebGPU | ~10s | ~10-20 t/s |
| Móvil Gama Media| WASM | ~20s | ~1 t/s |

## 5. Solución de Problemas

- **Error "WebGPU not supported"**: El sistema cambiará automáticamente a CPU.
- **Descarga lenta**: El modelo pesa ~300MB. La primera vez depende de la conexión. Las siguientes veces es instantáneo (caché).
- **Memoria insuficiente**: Si el navegador crashea en móviles, intenta usar modelos más pequeños (ej. `Xenova/gpt2`) o cerrar otras pestañas.
