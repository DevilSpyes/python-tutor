🐍 Python Tutor – Plataforma Interactiva de Aprendizaje de Python
Proyecto educativo gratuito y multiplataforma

Python Tutor es una plataforma interactiva que permite aprender Python desde cero hasta un nivel avanzado, con un enfoque práctico y ejercicios guiados. Todo se ejecuta en el navegador del usuario, evitando consumo de recursos en servidores y permitiendo uso desde móvil, PC y cualquier sistema operativo.

Incluye un panel de chat con IA que puede funcionar de dos formas:

IA ligera local (Lite) – corre en el navegador sin GPU siempre que sea posible.

IA mediante API externa (OpenAI/Anthropic/Qwen API) – el usuario introduce su propia clave.

La plataforma es estática y se despliega fácilmente en Netlify o cualquier hosting estático.

🚀 Características principales
✔ Ejecución de Python en el navegador
Gracias a Pyodide, todo el código Python se ejecuta en el navegador del alumno.
No requiere backend, servidores ni procesos externos.

✔ Consola interactiva + editor
La interfaz integra:

Editor de código

Terminal interactiva

Resultados en tiempo real

Ejercicios autoevaluados

✔ IA integrada
En el panel lateral derecho:

Puede funcionar con modelo Lite local (cuando el navegador lo soporte)

O con modelo API si el usuario coloca su clave

Se usa para resolver dudas, explicar errores y guiar al alumno

✔ Sistema de progreso
Los ejercicios se registran en localStorage del navegador, de forma que no necesitas base de datos.

✔ Curso modular
Incluye:

Módulo 00 → Bienvenida y guía

Módulos 01–XX → Ejercicios explicados, graduales, revisados

Volcado de todo el curriculum

Certificado final (opcional, local)

📘 Estructura del Proyecto
python_tutor/
│
├── static/                 # HTML, CSS y JS de la interfaz
├── curriculum/             # Todos los módulos y ejercicios
├── ai/                     # IA Lite y configuración de API
├── utils.py                # Funciones auxiliares
├── tutor.py                # Motor principal del curso
├── main.py                 # Punto de entrada
├── README.md               # Este archivo
├── requirements.txt        # Dependencias del entorno local
└── ...
🤖 IA Integrada
Opción A — IA Lite Local (sin WebGPU si es posible)
Se incluye un modelo ultra ligero alojado en /static/models/llm-lite.bin.

Ventajas:

No requiere GPU

No requiere API

No consume servidores externos

Funciona offline

Limitaciones:

Respuestas más simples

Funcionamiento variable según navegador

Esta IA se carga automáticamente si el navegador la soporta.

Opción B — IA vía API del usuario
En el panel de configuración, el alumno puede introducir:

Clave de OpenAI

Clave de Anthropic

Clave de Qwen API

Cualquier proveedor OpenAI-compatible

El modelo se usa sin almacenar la clave en servidores.

🧭 Guía rápida para estudiantes
Abre el curso en tu navegador

Lee el módulo de bienvenida

Completa cada ejercicio en orden

Usa el panel de IA para pedir explicaciones

Guarda tu progreso automáticamente

Avanza hasta el módulo final y genera tu certificado

🧑‍💻 Guía para desarrolladores
Para trabajar localmente:

git clone https://github.com/tuusuario/python-tutor.git
cd python_tutor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
🌐 Cómo desplegar en Netlify (paso a paso)
1. Crea un repositorio en GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TUUSUARIO/python-tutor.git
git push -u origin main
2. Entra a https://app.netlify.com
→ Click en New site from Git
→ Selecciona GitHub
→ Elige el repositorio

3. Configuración
Build command: (vacío)

Publish directory: static

Click Deploy site.

4. Listo
Netlify te dará una URL pública y gratuita como:

https://python-tutor.netlify.app
🧩 Cómo actualizar el contenido del curso
Los archivos del curso están en:

curriculum/
Cada archivo representa una lección o módulo.
Edita cualquiera y Netlify actualizará la web automáticamente cuando hagas push.

🛠 Mejoras futuras (ya preparadas para implementar)
Sistema de logros

Certificado oficial exportable

Modo práctica libre

Renderizado de gráficos Turtle dentro del navegador

IA local más robusta cuando WebGPU sea estándar

📄 Licencia
Proyecto libre, sin ánimo de lucro.
Todo el contenido puede ser reutilizado con atribución.
