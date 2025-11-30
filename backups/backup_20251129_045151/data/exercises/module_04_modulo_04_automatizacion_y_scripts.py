from data.exercises import Module, Lesson

MODULE = Module(
    id=4,
    title="Módulo 04: Automatización y Scripts",
    lessons=[
        Lesson(
            id=61,
            title="Avatar Básico",
            content='Estudia el siguiente código: Avatar Básico',
            example_code="# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\nfrom py_avataaars import PyAvataaar\n# Es posible que necesites instalar la librería cairo.\n# Para mac: escribe `brew install cairo`\navatar = PyAvataaar()\navatar.render_png_file('basic_avatar.png')\navatar.render_svg_file('basic_avatar.svg')\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=62,
            title="Avatar Personalizado",
            content='Estudia el siguiente código: Avatar Personalizado',
            example_code="# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\nimport py_avataaars as pa\n\navatar = pa.PyAvataaar(\n    style=pa.AvatarStyle.TRANSPARENT,\n    skin_color=pa.SkinColor.LIGHT,\n    hair_color=pa.HairColor.BLACK,\n    facial_hair_type=pa.FacialHairType.DEFAULT,\n    facial_hair_color=pa.HairColor.BLACK,\n    top_type=pa.TopType.SHORT_HAIR_SHORT_FLAT,\n    hat_color=pa.Color.BLACK,\n    mouth_type=pa.MouthType.SMILE,\n    eye_type=pa.EyesType.DEFAULT,\n    eyebrow_type=pa.EyebrowType.DEFAULT,\n    nose_type=pa.NoseType.DEFAULT,\n    accessories_type=pa.AccessoriesType.SUNGLASSES,\n    clothe_type=pa.ClotheType.SHIRT_V_NECK,\n    clothe_color=pa.Color.BLUE_03,\n    clothe_graphic_type=pa.ClotheGraphicType.BAT,\n)\navatar.render_png_file('avatar_custom.png')\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=63,
            title="Avatar Personalizado II",
            content='Estudia el siguiente código: Avatar Personalizado II',
            example_code='# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\nimport python_avatars as pa\n\npa.Avatar(\n    style=pa.AvatarStyle.TRANSPARENT,\n    # background_color=\'#FF00FF\',\n    # Choose graphic shirt\n    clothing=pa.ClothingType.GRAPHIC_SHIRT,\n    clothing_color=pa.ClothingColor.BLUE_01,\n    # Important to choose this as shirt_graphic, otherwise shirt_text will be ignored\n    shirt_graphic=pa.ClothingGraphic.CUSTOM_TEXT,\n    shirt_text=\'Flexmind\'\n).render("avatar_text.svg")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=64,
            title="Avatar Aleatorio",
            content='Estudia el siguiente código: Avatar Aleatorio',
            example_code='# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\nimport python_avatars as pa\n\n# Avatar completamente aleatorio\nrandom_avatar_1 = pa.Avatar.random()\n\n# Avatar aleatorio excepto el sombrero\nrandom_avatar_2 = pa.Avatar.random(top=pa.HatType.HAT)  # Más atributos pueden mantenerse fijos\n\n# Avatar fijo pero ropa aleatoria\nrandom_avatar_3 = pa.Avatar(\n    style=pa.AvatarStyle.CIRCLE,\n    hair_color=pa.HairColor.BLACK,\n    accessory=pa.AccessoryType.NONE,\n    clothing=pa.ClothingType.pick_random(), # La ropa se elige aleatoriamente\n)\n\n# Renderizar salida\nrandom_avatar_1.render("avatar_1.svg")\nprint("Guardado avatar_1.svg")\nrandom_avatar_2.render("avatar_2.svg")\nprint("Guardado avatar_2.svg")\nrandom_avatar_3.render("avatar_3.svg")\nprint("Guardado avatar_3.svg")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=65,
            title="Reloj Digital Básico",
            content='Estudia el siguiente código: Reloj Digital Básico',
            example_code='#!/usr/bin/python3\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Reloj Digital Básico (Versión Web)\n# Este script genera un archivo HTML con un reloj digital funcional.\n\nhtml_content = """\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #282c34; color: #61dafb; font-family: monospace; }\n.clock { font-size: 4rem; border: 4px solid #61dafb; padding: 20px; border-radius: 10px; box-shadow: 0 0 20px rgba(97, 218, 251, 0.5); }\n</style>\n<script>\nfunction updateClock() {\n    const now = new Date();\n    const timeString = now.toLocaleTimeString();\n    document.getElementById("clock").innerText = timeString;\n}\nsetInterval(updateClock, 1000);\nwindow.onload = updateClock;\n</script>\n</head>\n<body>\n<div id="clock" class="clock">Loading...</div>\n</body>\n</html>\n"""\n\nfilename = "reloj_digital.html"\nwith open(filename, "w") as f:\n    f.write(html_content)\n\nprint(f"Generado archivo: {filename}")\nprint("El reloj debería aparecer en la sección de archivos generados.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para generar el reloj.\n# 2. Modifica el CSS en la variable html_content para cambiar el color del reloj.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=66,
            title="Reloj Digital Avanzado",
            content='Estudia el siguiente código: Reloj Digital Avanzado',
            example_code='#!/usr/bin/python3\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Reloj Digital Avanzado (Temporizador Web)\n# Genera un temporizador de cuenta regresiva en HTML.\n\nseconds = 10 # Duración del temporizador\n\nhtml_content = f"""\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody {{ display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #222; color: #ff5555; font-family: "Courier New", monospace; }}\n.timer {{ font-size: 5rem; font-weight: bold; }}\n.message {{ font-size: 2rem; color: #50fa7b; display: none; }}\n</style>\n<script>\nlet timeLeft = {seconds};\nfunction updateTimer() {{\n    if (timeLeft <= 0) {{\n        document.getElementById("timer").style.display = "none";\n        document.getElementById("message").style.display = "block";\n        return;\n    }}\n    const mins = Math.floor(timeLeft / 60).toString().padStart(2, "0");\n    const secs = (timeLeft % 60).toString().padStart(2, "0");\n    document.getElementById("timer").innerText = `${{mins}}:${{secs}}`;\n    timeLeft--;\n}}\nsetInterval(updateTimer, 1000);\nwindow.onload = updateTimer;\n</script>\n</head>\n<body>\n<div id="timer" class="timer">00:00</div>\n<div id="message" class="message">¡TIEMPO TERMINADO!</div>\n</body>\n</html>\n"""\n\nfilename = "temporizador.html"\nwith open(filename, "w") as f:\n    f.write(html_content)\n\nprint(f"Generado archivo: {filename}")\nprint(f"Temporizador configurado para {seconds} segundos.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para generar el temporizador.\n# 2. Cambia la variable \'seconds\' para ajustar la duración.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=67,
            title="Reloj Digital CLI",
            content='Estudia el siguiente código: Reloj Digital CLI',
            example_code='#!/usr/bin/python3\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Reloj Digital con Fecha (Versión Web)\n# Genera un reloj que muestra fecha y hora.\n\nhtml_content = """\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #000; color: #0f0; font-family: "Consolas", monospace; }\n.time { font-size: 6rem; text-shadow: 0 0 10px #0f0; }\n.date { font-size: 2rem; color: #0a0; margin-top: 10px; }\n</style>\n<script>\nfunction updateClock() {\n    const now = new Date();\n    document.getElementById("time").innerText = now.toLocaleTimeString();\n    document.getElementById("date").innerText = now.toLocaleDateString(undefined, { weekday: "long", year: "numeric", month: "long", day: "numeric" });\n}\nsetInterval(updateClock, 1000);\nwindow.onload = updateClock;\n</script>\n</head>\n<body>\n<div id="time" class="time">--:--:--</div>\n<div id="date" class="date">Loading date...</div>\n</body>\n</html>\n"""\n\nfilename = "reloj_fecha.html"\nwith open(filename, "w") as f:\n    f.write(html_content)\n\nprint(f"Generado archivo: {filename}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Modifica el estilo CSS para cambiar el color del texto a rojo (#f00).\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=68,
            title="Reloj Mundial",
            content='Estudia el siguiente código: Reloj Mundial',
            example_code='#!/usr/bin/python3\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Reloj Mundial (Versión Web)\n# Genera un tablero con múltiples zonas horarias.\n\nhtml_content = """\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }\n.container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; width: 80%; max-width: 1000px; }\n.clock-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }\n.city { font-size: 1.2rem; color: #666; margin-bottom: 10px; font-weight: bold; }\n.time { font-size: 2rem; color: #333; font-family: monospace; }\n</style>\n<script>\nconst zones = [\n    { city: "New York", zone: "America/New_York" },\n    { city: "London", zone: "Europe/London" },\n    { city: "Tokyo", zone: "Asia/Tokyo" },\n    { city: "Sydney", zone: "Australia/Sydney" },\n    { city: "India", zone: "Asia/Kolkata" }\n];\n\nfunction updateClocks() {\n    const now = new Date();\n    zones.forEach(item => {\n        const timeString = now.toLocaleTimeString("en-US", { timeZone: item.zone });\n        document.getElementById(item.city).innerText = timeString;\n    });\n}\nsetInterval(updateClocks, 1000);\nwindow.onload = updateClocks;\n</script>\n</head>\n<body>\n<div class="container">\n    <div class="clock-card"><div class="city">New York</div><div id="New York" class="time">--:--:--</div></div>\n    <div class="clock-card"><div class="city">London</div><div id="London" class="time">--:--:--</div></div>\n    <div class="clock-card"><div class="city">Tokyo</div><div id="Tokyo" class="time">--:--:--</div></div>\n    <div class="clock-card"><div class="city">Sydney</div><div id="Sydney" class="time">--:--:--</div></div>\n    <div class="clock-card"><div class="city">India</div><div id="India" class="time">--:--:--</div></div>\n</div>\n</body>\n</html>\n"""\n\nfilename = "reloj_mundial.html"\nwith open(filename, "w") as f:\n    f.write(html_content)\n\nprint(f"Generado archivo: {filename}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para ver el reloj mundial.\n# 2. Intenta añadir una nueva tarjeta para otra ciudad en el HTML.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=69,
            title="Captura de Cámara (OpenCV - Headless)",
            content='Estudia el siguiente código: Captura de Cámara (OpenCV - Headless)',
            example_code='# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# capturar una sola imagen de la webcam usando python\n# Nota: En un entorno servidor/web, no podemos abrir una ventana (imshow).\n# En su lugar, guardamos la imagen en un archivo.\n\nimport cv2 as cv\nimport time\nimport os\n\n# inicializar la cámara\n# Si no hay cámara física, esto podría fallar o devolver un frame negro.\ncam_port = 0\n\nprint("Inicializando cámara...")\ntry:\n    cam = cv.VideoCapture(cam_port)\n    \n    # esperar a que la cámara se caliente\n    time.sleep(1)\n\n    # leyendo la entrada usando la cámara\n    result, image = cam.read()\n\n    # Si la imagen se detecta sin errores, mostrar resultado\n    if result:\n        # guardando imagen en almacenamiento local\n        filename = "cam_capture.jpg"\n        cv.imwrite(filename, image)\n        print(f"¡Foto tomada! Guardada como {filename}")\n    else:\n        print("No se pudo acceder a la cámara. (Es normal en servidores sin webcam)")\n        \nexcept Exception as e:\n    print(f"Error de cámara: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Si falla (sin webcam), intenta cargar una imagen existente con cv.imread() y guardarla con otro nombre.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=70,
            title="Imagen a Caricatura (Real)",
            content='Estudia el siguiente código: Imagen a Caricatura (Real)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Procesamiento de Imagen Real con PIL\n# Primero generamos una imagen base y luego aplicamos filtros.\n\nimport py_avataaars as pa\nfrom PIL import Image, ImageFilter, ImageOps\nimport os\n\nprint("--- Generando imagen base ---")\n# 1. Generar un avatar como imagen base\navatar = pa.PyAvataaar(\n    style=pa.AvatarStyle.CIRCLE,\n    skin_color=pa.SkinColor.LIGHT,\n    hair_color=pa.HairColor.BROWN,\n    facial_hair_type=pa.FacialHairType.DEFAULT,\n    top_type=pa.TopType.SHORT_HAIR_SHORT_FLAT,\n    mouth_type=pa.MouthType.SMILE,\n    eye_type=pa.EyesType.DEFAULT\n)\navatar.render_png_file(\'base_image.png\')\nprint("Imagen base guardada: base_image.png")\n\n# 2. Procesar con PIL (Pillow)\nprint("--- Aplicando efectos de caricatura ---")\ntry:\n    img = Image.open(\'base_image.png\').convert("RGB")\n    \n    # Aplicar filtro de bordes (Contour)\n    edges = img.filter(ImageFilter.CONTOUR)\n    \n    # Aplicar suavizado\n    smooth = img.filter(ImageFilter.SMOOTH_MORE)\n    \n    # Combinar para efecto "cartoon" simple\n    cartoon = Image.blend(smooth, edges, 0.5)\n    \n    # Guardar resultado\n    output_file = "cartoon_result.png"\n    cartoon.save(output_file)\n    print(f"¡Éxito! Caricatura guardada como: {output_file}")\n    \nexcept Exception as e:\n    print(f"Error procesando imagen: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para ver el resultado real.\n# 2. Cambia ImageFilter.CONTOUR por ImageFilter.EMBOSS o ImageFilter.FIND_EDGES.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=71,
            title="Caricatura con GUI (Web)",
            content='Estudia el siguiente código: Caricatura con GUI (Web)',
            example_code='#!/usr/bin/python3\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Editor de Caricaturas (Interfaz Web)\n# Genera una interfaz HTML para aplicar filtros a una imagen.\n\nhtml_content = """\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody { font-family: sans-serif; text-align: center; background-color: #222; color: white; padding: 20px; }\n.container { background: #333; padding: 20px; border-radius: 10px; display: inline-block; }\nimg { max-width: 100%; border-radius: 5px; transition: filter 0.3s; margin-bottom: 20px; border: 2px solid #555; }\n.controls { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }\nbutton { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; background-color: #007bff; color: white; font-size: 16px; }\nbutton:hover { background-color: #0056b3; }\n</style>\n<script>\nfunction applyFilter(filter) {\n    const img = document.getElementById(\'targetImage\');\n    img.style.filter = filter;\n}\n</script>\n</head>\n<body>\n<div class="container">\n    <h1>Editor de Caricaturas Web</h1>\n    <!-- Usamos una imagen de ejemplo -->\n    <img id="targetImage" src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=Hoodie&clotheColor=Blue03&eyeType=Happy&eyebrowType=Default&mouthType=Smile&skinColor=Light" alt="Avatar">\n    \n    <div class="controls">\n        <button onclick="applyFilter(\'none\')">Normal</button>\n        <button onclick="applyFilter(\'grayscale(100%)\')">B/N</button>\n        <button onclick="applyFilter(\'sepia(100%)\')">Sepia</button>\n        <button onclick="applyFilter(\'contrast(200%)\')">Alto Contraste</button>\n        <button onclick="applyFilter(\'invert(100%)\')">Invertir</button>\n        <button onclick="applyFilter(\'blur(5px)\')">Desenfoque</button>\n        <button onclick="applyFilter(\'saturate(300%)\')">Saturado</button>\n        <button onclick="applyFilter(\'hue-rotate(90deg)\')">Alien</button>\n    </div>\n</div>\n</body>\n</html>\n"""\n\nfilename = "editor_caricatura.html"\nwith open(filename, "w") as f:\n    f.write(html_content)\n\nprint(f"Generado archivo: {filename}")\nprint("La interfaz gráfica aparecerá en la sección de archivos generados.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para generar la interfaz.\n# 2. Añade un nuevo botón en el HTML para un filtro diferente (ej. brightness).\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=72,
            title="Generador QR (API Real)",
            content='Estudia el siguiente código: Generador QR (API Real)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Generador de QR usando una API pública\n# No requiere instalar librerías complejas.\n\nimport requests\n\ndata = "https://www.python.org"\nsize = "300x300"\napi_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}&data={data}"\n\nprint(f"Generando QR para: {data}")\nprint("Contactando API...")\n\ntry:\n    response = requests.get(api_url)\n    if response.status_code == 200:\n        filename = "qr_code.png"\n        with open(filename, "wb") as f:\n            f.write(response.content)\n        print(f"¡Éxito! QR guardado como: {filename}")\n    else:\n        print("Error en la API.")\nexcept Exception as e:\n    print(f"Error de conexión: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Cambia la variable \'data\' por tu propio texto o URL.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=73,
            title="Info de Imagen (PIL)",
            content='Estudia el siguiente código: Info de Imagen (PIL)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Análisis de Imagen con Pillow (PIL)\n\nfrom PIL import Image\nimport os\n\n# Usamos una imagen generada previamente o descargada\nfilename = "qr_code.png"\n\nif not os.path.exists(filename):\n    print(f"El archivo {filename} no existe. Ejecuta la lección anterior primero.")\nelse:\n    try:\n        with Image.open(filename) as img:\n            print("--- Información de la Imagen ---")\n            print(f"Archivo: {filename}")\n            print(f"Formato: {img.format}")\n            print(f"Modo: {img.mode}")\n            print(f"Tamaño: {img.size} (Ancho: {img.width}, Alto: {img.height})")\n            \n            # Operación simple: Convertir a escala de grises\n            grayscale = img.convert("L")\n            grayscale.save("qr_grayscale.png")\n            print("Imagen convertida a escala de grises guardada como \'qr_grayscale.png\'")\n            \n    except Exception as e:\n        print(f"Error procesando imagen: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Intenta rotar la imagen usando img.rotate(90).\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=74,
            title="Análisis de Texto (Frecuencia)",
            content='Estudia el siguiente código: Análisis de Texto (Frecuencia)',
            example_code='#!/usr/bin/python\n# Análisis de Frecuencia de Palabras\n\nfrom collections import Counter\nimport re\n\ntexto = """\nPython es un lenguaje de programación interpretado cuya filosofía hace hincapié \nen la legibilidad de su código. Se trata de un lenguaje de programación multiparadigma, \nya que soporta orientación a objetos, programación imperativa y, en menor medida, \nprogramación funcional. Es un lenguaje interpretado, dinámico y multiplataforma.\n"""\n\nprint("--- Texto Original ---")\nprint(texto.strip())\nprint("-" * 20)\n\n# Limpieza básica: minúsculas y eliminar puntuación\nlimpio = re.sub(r"[^\\w\\s]", "", texto.lower())\npalabras = limpio.split()\n\nprint(f"Total de palabras: {len(palabras)}")\n\n# Contar frecuencia\nconteo = Counter(palabras)\n\nprint("\\n--- Palabras más comunes ---")\nfor palabra, cantidad in conteo.most_common(5):\n    print(f"{palabra}: {cantidad}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Añade más texto a la variable \'texto\' y observa cómo cambia el conteo.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=75,
            title="Análisis de Sentimiento (Simple)",
            content='Estudia el siguiente código: Análisis de Sentimiento (Simple)',
            example_code='#!/usr/bin/python\n# Analizador de Sentimiento Básico (Basado en palabras clave)\n\npositivas = ["bueno", "excelente", "increíble", "feliz", "amor", "gusta", "genial"]\nnegativas = ["malo", "terrible", "triste", "odio", "feo", "error", "fallo"]\n\ndef analizar_sentimiento(texto):\n    texto = texto.lower()\n    score = 0\n    \n    for p in positivas:\n        if p in texto:\n            score += 1\n            \n    for n in negativas:\n        if n in texto:\n            score -= 1\n            \n    return score\n\nfrases = [\n    "Python es increíble y genial",\n    "Este error es terrible y feo",\n    "Hoy es un día normal"\n]\n\nprint("--- Análisis de Sentimiento ---")\nfor frase in frases:\n    score = analizar_sentimiento(frase)\n    veredicto = "Neutro"\n    if score > 0: veredicto = "Positivo"\n    if score < 0: veredicto = "Negativo"\n    \n    print(f"Frase: \'{frase}\' | Score: {score} ({veredicto})")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Añade tus propias frases a la lista y ve cómo se clasifican.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=76,
            title="Validador de Email (Regex)",
            content='Estudia el siguiente código: Validador de Email (Regex)',
            example_code='#!/usr/bin/python\n# Validación de Email con Expresiones Regulares\n\nimport re\n\n# Regex estándar para email\nemail_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"\n\nemails = [\n    "usuario@example.com",\n    "nombre.apellido@empresa.co.uk",\n    "invalido@com",\n    "sin_arroba.com",\n    "user@domain"\n]\n\nprint("--- Validador de Emails ---")\nfor email in emails:\n    if re.match(email_regex, email):\n        print(f"[VALIDO]   {email}")\n    else:\n        print(f"[INVALIDO] {email}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Intenta mejorar la regex o probar con otros emails.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=77,
            title="Generador PDF (Reporte)",
            content='Estudia el siguiente código: Generador PDF (Reporte)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Generación de un Reporte PDF Simple\n# REQUISITO: pip install fpdf2\n\nfrom fpdf import FPDF\n\nprint("Generando reporte PDF...")\n\npdf = FPDF()\npdf.add_page()\n\n# Título\n# Usamos Helvetica que es una fuente core estándar para evitar advertencias\npdf.set_font("helvetica", "B", 16)\npdf.cell(40, 10, "Reporte de Actividad")\npdf.ln(20)\n\n# Contenido\npdf.set_font("helvetica", "", 12)\n# ln=1 está deprecado en fpdf2, usamos new_x="LMARGIN", new_y="NEXT"\npdf.cell(0, 10, "Este es un documento generado automáticamente con Python.", new_x="LMARGIN", new_y="NEXT")\npdf.cell(0, 10, "Podemos añadir texto, líneas y números.", new_x="LMARGIN", new_y="NEXT")\n\nfor i in range(1, 6):\n    pdf.cell(0, 10, f"Línea de detalle número {i}", new_x="LMARGIN", new_y="NEXT")\n\nfilename = "reporte_simple.pdf"\npdf.output(filename)\nprint(f"¡PDF guardado como {filename}!")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n# 2. Añade una línea final que diga "Fin del Reporte" en negrita.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=78,
            title="Texto a Voz Simple",
            content='Estudia el siguiente código: Texto a Voz Simple',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Texto a Voz Simple\n# REQUISITO: pip install pyttsx3\n\nimport pyttsx3\n\nengine = pyttsx3.init() # creación del objeto\n\n""" VELOCIDAD """\nrate = engine.getProperty(\'rate\')   # obteniendo detalles de la velocidad actual, por defecto es 200\n#engine.setProperty(\'rate\', 125) # Configurando nueva velocidad de voz\n\n""" VOLUMEN """\nvolume = engine.getProperty(\'volume\')   # conociendo el nivel de volumen actual (min=0 y max=1)\nengine.setProperty(\'volume\',0.9)    # configurando nivel de volumen entre 0 y 1\n\n""" VOZ """\nvoices = engine.getProperty(\'voices\')       # obteniendo detalles de la voz actual\n# engine.setProperty(\'voice\', voices[0].id)  # cambiando índice, cambia voces. 0 para hombre\n# engine.setProperty(\'voice\', voices[1].id)   # cambiando índice, cambia voces. 1 para mujer\n\nengine.say("¡Hola Mundo!")\nengine.say(\'Mi velocidad actual es \' + str(rate))\nengine.runAndWait()\nengine.stop()\n\n""" Guardando Voz en un archivo """\n# En linux asegúrate de que \'espeak\' y \'ffmpeg\' están instalados\nengine.save_to_file(\'Hola Mundo\', \'test.mp3\')\nengine.runAndWait()\n\n\'\'\'\nvoices = engine.getProperty(\'voices\')\nfor voice in voices:\n    print("Voz: %s" % voice.name)\n    print(" - ID: %s" % voice.id)\n    print(" - Idiomas: %s" % voice.languages)\n    print(" - Género: %s" % voice.gender)\n    print(" - Edad: %s" % voice.age)\n    print("\\n")\n\n# https://pyttsx3.readthedocs.io/en/latest/\n# https://pyttsx3.readthedocs.io/en/latest/engine.html#examples\n\'\'\'\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=79,
            title="Espiral Arcoíris (SVG Turtle)",
            content='Estudia el siguiente código: Espiral Arcoíris (SVG Turtle)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Espiral Arcoíris (SVG Turtle)\n# REQUISITO: pip install svg_turtle\n\nfrom svg_turtle import SvgTurtle\n\nt = SvgTurtle(width=500, height=500)\nt.bgcolor(\'black\')\nt.speed = 0 # Ignorado en SVG pero mantenido por compatibilidad\n\ncolors = [\'red\', \'purple\', \'blue\', \'green\', \'orange\', \'yellow\']\n\nprint(\'Generando espiral...\')\nfor x in range(360):\n    t.pencolor(colors[x % 6])\n    t.width = x / 100 + 1\n    t.forward(x)\n    t.left(59)\n\nfilename = \'espiral_turtle.svg\'\nt.save_as(filename)\nprint(f\'¡Dibujo guardado como {filename}!\')\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n# 2. Cambia el ángulo t.left(59) a 90 o 91 para ver patrones diferentes.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=80,
            title="Triángulo de Sierpinski (SVG)",
            content='Estudia el siguiente código: Triángulo de Sierpinski (SVG)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Triángulo de Sierpinski (SVG)\n# REQUISITO: pip install svg_turtle\n\nfrom svg_turtle import SvgTurtle\n\ndef draw_triangle(t, points, color):\n    # Dibujo simple de triángulo con líneas\n    t.pencolor(color)\n    t.penup()\n    t.goto(points[0][0], points[0][1])\n    t.pendown()\n    t.goto(points[1][0], points[1][1])\n    t.goto(points[2][0], points[2][1])\n    t.goto(points[0][0], points[0][1])\n\ndef get_mid(p1, p2):\n    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)\n\ndef sierpinski(points, degree, t):\n    colormap = [\'blue\', \'red\', \'green\', \'white\', \'yellow\', \'violet\', \'orange\']\n    draw_triangle(t, points, colormap[degree])\n    \n    if degree > 0:\n        sierpinski([points[0], \n                    get_mid(points[0], points[1]), \n                    get_mid(points[0], points[2])], \n                   degree-1, t)\n        sierpinski([points[1], \n                    get_mid(points[0], points[1]), \n                    get_mid(points[1], points[2])], \n                   degree-1, t)\n        sierpinski([points[2], \n                    get_mid(points[2], points[1]), \n                    get_mid(points[0], points[2])], \n                   degree-1, t)\n\nt = SvgTurtle(width=400, height=400)\npoints = [[-100, -50], [0, 100], [100, -50]]\n\nprint(\'Generando Sierpinski...\')\nsierpinski(points, 3, t)\n\nfilename = \'sierpinski.svg\'\nt.save_as(filename)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n# 2. Cambia el grado de recursión de 3 a 4 (cuidado, crece exponencialmente).\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=81,
            title="Arte Geométrico (SVG)",
            content='Estudia el siguiente código: Arte Geométrico (SVG)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Arte Geométrico (SVG)\n# REQUISITO: pip install svg_turtle\n\nfrom svg_turtle import SvgTurtle\n\ndef draw_square(t):\n    for i in range(4):\n        t.forward(100)\n        t.right(90)\n\nt = SvgTurtle(width=500, height=500)\nt.pencolor(\'blue\')\n\nprint(\'Generando arte geométrico...\')\nfor i in range(36):\n    draw_square(t)\n    t.right(10)\n\nfilename = \'arte_geo.svg\'\nt.save_as(filename)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n# 2. Cambia el ángulo de rotación o el tamaño del cuadrado.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=82,
            title="Cuadrado y Círculo (SVG)",
            content='Estudia el siguiente código: Cuadrado y Círculo (SVG)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Cuadrado y Círculo (SVG)\n# REQUISITO: pip install svg_turtle\n\nfrom svg_turtle import SvgTurtle\nimport math\n\ndef draw_circle_approx(t, radius):\n    # Aproximación de círculo con líneas\n    circumference = 2 * math.pi * radius\n    step_length = circumference / 36\n    for _ in range(36):\n        t.forward(step_length)\n        t.right(10)\n\nt = SvgTurtle(width=400, height=400)\n\n# Cuadrado\nt.pencolor("red")\nfor _ in range(4):\n    t.forward(100)\n    t.right(90)\n\n# Círculo (Aproximado)\nt.penup()\nt.goto(50, 50)\nt.pendown()\nt.pencolor("blue")\ndraw_circle_approx(t, 50)\n\nfilename = "shapes.svg"\nt.save_as(filename)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=83,
            title="Cuadrado Simple (SVG)",
            content='Estudia el siguiente código: Cuadrado Simple (SVG)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Cuadrado Simple (SVG)\n# REQUISITO: pip install svg_turtle\n\nfrom svg_turtle import SvgTurtle\n\nt = SvgTurtle()\nt.pencolor("green")\n\nprint("Dibujando cuadrado...")\nt.forward(100)\nt.right(90)\nt.forward(100)\nt.right(90)\nt.forward(100)\nt.right(90)\nt.forward(100)\nt.right(90)\n\nt.save_as("cuadrado.svg")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=84,
            title="Colores en Terminal (Colorama)",
            content='Estudia el siguiente código: Colores en Terminal (Colorama)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Colores en Terminal con Colorama\n# REQUISITO: pip install colorama\n\nfrom colorama import init, Fore, Back, Style\ninit(autoreset=True)\n\n\nprint(Fore.RED + \'texto rojo\')\nprint(Fore.GREEN + \'texto verde\')\nprint(Fore.BLUE + \'texto azul\')\nprint(Fore.CYAN + \'texto cian\')\nprint(Fore.MAGENTA + \'texto magenta\')\nprint(Back.GREEN + \'y con fondo verde\')\nprint(Style.DIM + \'y en texto tenue\')\nprint(Style.BRIGHT + Fore.GREEN + \'y color verde en texto brillante\')\nprint(\'automáticamente de vuelta al color por defecto\')\n\n\n\n# Estos son los colores disponibles\n"""\nFore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.\nBack: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.\nStyle: DIM, NORMAL, BRIGHT, RESET_ALL\n"""\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=85,
            title="Descargar Archivos",
            content='Estudia el siguiente código: Descargar Archivos',
            example_code='import sys\nimport requests\nimport re\nfrom colorama import init, Fore, Back, Style\nimport validators\n\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# PROPÓSITO de este script\n# Obtener una url con varios formatos de archivos para descargar\n\ninit(autoreset=True)\n\n# --- CORRECCIÓN PARA EJECUCIÓN WEB ---\n# Simulando argumentos de línea de comandos si no se proporcionan\nif len(sys.argv) < 2:\n    print(Fore.YELLOW + "No se proporcionaron argumentos. Usando URL por defecto para demo.")\n    sys.argv.append("https://www.python.org/static/img/python-logo.png")\n# --------------------------\n\nfile_url = sys.argv[1]\n\nif not validators.url(file_url):\n    print(Fore.RED + Style.BRIGHT + "URL no válida")\n    # exit() eliminado para prevenir caída del servidor\nelse:\n    # extraer nombre de archivo de la url\n    matched_file = re.search("(?=[\\\\w\\\\d-]+\\\\.\\\\w{3,4}$).+", file_url)\n    if matched_file is not None:\n        file_name_with_extension = matched_file.group(0)\n    else:\n        file_name_with_extension = "downloaded_file.png"\n        \n    print("Descargando %s" % file_name_with_extension)\n\n    try:\n        response = requests.get(file_url, stream = True)\n        with open(file_name_with_extension, "wb") as file_download:\n            total_length = response.headers.get(\'content-length\')\n            if total_length:\n                total_length = int(total_length)\n                print("El tamaño total del archivo es: {0:.3f} KB".format(total_length/1024))\n            else:\n                print("Tamaño total desconocido.")\n                total_length = 1000 # Valor dummy\n\n            dl_bar = 0\n            for chunk in response.iter_content(chunk_size = 1024):\n                if chunk:\n                    dl_bar += len(chunk)\n                    file_download.write(chunk)\n                    done = int(50 * dl_bar / total_length)\n                    sys.stdout.write(Fore.GREEN + Style.BRIGHT + "\\r[%s%s]" % (\'=\' * done, \' \' * (50-done)) )\n                    sys.stdout.flush()\n        print("\\n¡Descarga Completa! \\n")\n    except Exception as e:\n        print(f"Error descargando: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=86,
            title="Generar OTP",
            content='Estudia el siguiente código: Generar OTP',
            example_code='#!/usr/bin/python\n# Generar OTP de 6 dígitos\nimport string\nimport secrets\n\nnumber = string.digits\notp = \'\'\n\nfor i in range(6):\n    otp += \'\'.join(secrets.choice(number))\n\nprint(f\'Tu OTP es: {otp}\')\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=87,
            title="Generador de Contraseñas",
            content='Estudia el siguiente código: Generador de Contraseñas',
            example_code='import string\nimport secrets\n\ndef get_alphabet():\n    letters = string.ascii_letters\n    digits = string.digits\n    special_chars = string.punctuation\n    alphabet = letters + digits + special_chars\n    return alphabet\n\n# Restricciones de contraseña\npassword_len = 12 \nprint(f"Generando contraseña de longitud: {password_len}")\n\nif password_len <8:\n    print("La longitud debe ser de al menos 8 caracteres")\nelse:\n    password = \'\'\n    for i in range(password_len):\n        password += \'\'.join(secrets.choice(get_alphabet()))\n\n    print(f"La contraseña es: {password}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=88,
            title="Extraer Links de Web",
            content='Estudia el siguiente código: Extraer Links de Web',
            example_code='import requests\nimport sys\nimport re\nfrom bs4 import BeautifulSoup as bs\nimport validators\n\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n\n# --- CORRECCIÓN PARA EJECUCIÓN WEB ---\nif len(sys.argv) < 2:\n    print("No se proporcionó URL. Usando por defecto: https://www.python.org")\n    sys.argv.append("https://www.python.org")\n# --------------------------\n\nurl = sys.argv[1]\n\nif not validators.url(url):\n    print("URL no válida")\nelse:\n    try:\n        print(f"Obteniendo {url}...")\n        get_content = requests.get(url)\n        getpage_soup = bs(get_content.text, \'html.parser\')\n\n        all_links= getpage_soup.findAll(\'a\', attrs={\'href\' : re.compile("^https?://")})\n\n        domain_name = url.split(\'//\')[1]\n        print(f"Nombre de dominio: {domain_name}")\n        \n        print(f"Encontrados {len(all_links)} enlaces. Mostrando los primeros 5:")\n        for i, link in enumerate(all_links[:5]):\n            print(f"- {link.get(\'href\')}")\n            \n    except Exception as e:\n        print(f"Error: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=89,
            title="Info Usuario GitHub",
            content='Estudia el siguiente código: Info Usuario GitHub',
            example_code='import json\nimport requests\nimport sys\n\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n\n# --- CORRECCIÓN PARA EJECUCIÓN WEB ---\nif len(sys.argv) < 2:\n    print("No se proporcionó usuario. Usando por defecto: octocat")\n    sys.argv.append("octocat")\n# --------------------------\n\nusername = sys.argv[1]\napi_url_base = \'https://api.github.com/\'\nheaders = {\'Content-Type\': \'application/json\', \'User-Agent\': \'Python Student\', \'Accept\': \'application/vnd.github.v3+json\'}\n\ndef get_user_details(username):\n    user_url = \'{}users/{}\'.format(api_url_base, username)\n    response = requests.get(user_url, headers=headers)\n    if response.status_code == 200:\n        return response.content\n    else:\n        return None\n\nprint(f"Obteniendo info para el usuario: {username}")\nuser_details = get_user_details(username)\n\nif user_details:\n    user_in_json = user_details.decode(\'utf-8\')\n    user_detail_dict = json.loads(user_in_json)\n    print("="*10 + " Detalles de Usuario " + "="*10)\n    print("Nombre: {}".format(user_detail_dict.get(\'name\', \'N/A\')))\n    print("Bio: {}".format(user_detail_dict.get(\'bio\', \'N/A\')))\n    print("Ubicación: {}".format(user_detail_dict.get(\'location\', \'N/A\')))\n    print("Repos Públicos: {}".format(user_detail_dict.get(\'public_repos\', \'N/A\')))\nelse:\n    print("Usuario no encontrado.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=90,
            title="Convertir HEIC a PNG",
            content='Estudia el siguiente código: Convertir HEIC a PNG',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Convierte imágenes HEIC a PNG usando pillow-heif\n# REQUISITO: pip install pillow-heif\n\nfrom PIL import Image\nimport os\n\n# Intentamos importar pillow_heif, si no está, avisamos\ntry:\n    from pillow_heif import register_heif_opener\n    register_heif_opener()\n    HAS_HEIF = True\nexcept ImportError:\n    HAS_HEIF = False\n    print("NOTA: Instala \'pillow-heif\' para soporte real de HEIC.")\n\ndef convert_heic_to_png(heic_path):\n    if not os.path.exists(heic_path):\n        print(f"Archivo no encontrado: {heic_path}")\n        return\n\n    if not HAS_HEIF:\n        print("Librería pillow-heif no encontrada. No se puede convertir.")\n        return\n\n    print(f"Convirtiendo {heic_path}...")\n    try:\n        image = Image.open(heic_path)\n        png_path = heic_path.lower().replace(".heic", ".png")\n        image.save(png_path, format="PNG")\n        print(f"Guardado como: {png_path}")\n    except Exception as e:\n        print(f"Error al convertir: {e}")\n\n# Creamos un archivo dummy para probar si no existe\nif not os.path.exists("test.heic"):\n    print("Creando archivo dummy test.heic para demostración...")\n    # En realidad creamos un JPG y lo renombramos para que el script intente abrirlo\n    # (Fallará si es un JPG real pero esperamos HEIC, pero sirve para demo de flujo)\n    img = Image.new(\'RGB\', (100, 100), color = \'red\')\n    img.save(\'test.heic\') # Esto no es un HEIC válido, pero permite correr el script\n\nconvert_heic_to_png("test.heic")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Instala la librería: pip install pillow-heif\n# 2. Usa una foto real de iPhone (.HEIC) y prueba el script.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Necesitas instalar pillow-heif para que funcione con archivos reales.",
            type="interactive"
        ),
        Lesson(
            id=91,
            title="Rangos IP (JSON)",
            content='Estudia el siguiente código: Rangos IP (JSON)',
            example_code='import json\n\n# Datos truncados para brevedad\ndata = {\n  "syncToken": "1721411590",\n  "createDate": "2024-07-19-17-53-10",\n  "prefixes": [\n    {\n      "ip_prefix": "3.5.140.0/22",\n      "region": "ap-northeast-2",\n      "service": "AMAZON",\n      "network_border_group": "ap-northeast-2"\n    },\n    {\n      "ip_prefix": "13.34.1.109/32",\n      "region": "ap-southeast-2",\n      "service": "AMAZON",\n      "network_border_group": "ap-southeast-2"\n    }\n  ]\n}\n\nprint(json.dumps(data, indent=2))\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=92,
            title="Scraping con Selenium",
            content='Estudia el siguiente código: Scraping con Selenium',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Scraping real con Selenium\n# REQUISITO: pip install selenium webdriver-manager\n\nimport time\nfrom selenium import webdriver\nfrom selenium.webdriver.chrome.service import Service\nfrom webdriver_manager.chrome import ChromeDriverManager\nfrom selenium.webdriver.common.by import By\n\ndef run_scraper():\n    print("Iniciando Chrome...")\n    # Configuración para modo headless (sin ventana gráfica)\n    options = webdriver.ChromeOptions()\n    options.add_argument("--headless")\n    options.add_argument("--no-sandbox")\n    options.add_argument("--disable-dev-shm-usage")\n\n    try:\n        # Instalación automática del driver\n        service = Service(ChromeDriverManager().install())\n        driver = webdriver.Chrome(service=service, options=options)\n\n        url = "https://books.toscrape.com/"\n        print(f"Navegando a {url}...")\n        driver.get(url)\n\n        print("Extrayendo títulos de libros...")\n        # Buscamos elementos h3 > a\n        books = driver.find_elements(By.CSS_SELECTOR, "h3 a")\n        \n        for i, book in enumerate(books[:5], 1):\n            title = book.get_attribute("title")\n            print(f"{i}. {title}")\n\n        driver.quit()\n        print("¡Scraping completado!")\n\n    except Exception as e:\n        print(f"Error al ejecutar Selenium: {e}")\n        print("Asegúrate de tener Chrome instalado en tu sistema.")\n\n# Ejecutar\nrun_scraper()\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Este código requiere un entorno local con Chrome instalado.\n# 2. Instala las librerías necesarias y ejecútalo en tu IDE.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Selenium automatiza navegadores reales. Requiere el navegador instalado.",
            type="interactive"
        ),
        Lesson(
            id=93,
            title="Análisis de Datos CSV",
            content='Estudia el siguiente código: Análisis de Datos CSV',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Analizar un archivo CSV real\nimport csv\nimport os\n\n# Creamos un archivo CSV de prueba\ncsv_file = "datos_ventas.csv"\nwith open(csv_file, "w", newline="") as f:\n    writer = csv.writer(f)\n    writer.writerow(["Producto", "Precio", "Cantidad"])\n    writer.writerow(["Laptop", 1200, 5])\n    writer.writerow(["Mouse", 25, 50])\n    writer.writerow(["Teclado", 45, 30])\n    writer.writerow(["Monitor", 300, 10])\n\nprint(f"Analizando {csv_file}...")\n\ntotal_ventas = 0\nproductos_stock = 0\n\nwith open(csv_file, "r") as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        precio = float(row["Precio"])\n        cantidad = int(row["Cantidad"])\n        total = precio * cantidad\n        total_ventas += total\n        productos_stock += cantidad\n        print(f"Producto: {row[\'Producto\']} - Total: ${total}")\n\nprint("-" * 30)\nprint(f"Ventas Totales: ${total_ventas}")\nprint(f"Total Productos: {productos_stock}")\n\n# Limpieza\nos.remove(csv_file)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Modifica el código para calcular el precio promedio.\n# 2. Añade más productos al archivo CSV.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="La librería csv facilita la lectura y escritura de datos tabulares.",
            type="interactive"
        ),
        Lesson(
            id=94,
            title="Manipulación de PDF",
            content='Estudia el siguiente código: Manipulación de PDF',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Manipulación real de PDF usando pypdf\n# REQUISITO: pip install pypdf\n\nfrom pypdf import PdfReader, PdfWriter\nimport os\n\n# Crear un PDF simple para la demo (usando fpdf2 si está disponible, o simulando creación)\ntry:\n    from fpdf import FPDF\n    pdf = FPDF()\n    pdf.add_page()\n    pdf.set_font("helvetica", size=12)\n    pdf.cell(text="Hola Mundo PDF!", new_x="LMARGIN", new_y="NEXT")\n    pdf.output("demo.pdf")\n    HAS_FPDF = True\nexcept ImportError:\n    HAS_FPDF = False\n    print("Instala fpdf2 para generar el PDF de prueba.")\n\nif os.path.exists("demo.pdf"):\n    print("Leyendo demo.pdf...")\n    reader = PdfReader("demo.pdf")\n    print(f"Número de páginas: {len(reader.pages)}")\n    \n    page = reader.pages[0]\n    text = page.extract_text()\n    print("Texto extraído:")\n    print(text)\n    \n    # Crear un nuevo PDF con solo la primera página\n    writer = PdfWriter()\n    writer.add_page(page)\n    \n    with open("demo_copia.pdf", "wb") as f:\n        writer.write(f)\n    print("Copia guardada como demo_copia.pdf")\nelse:\n    print("No se encontró demo.pdf para leer.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Instala pypdf: pip install pypdf\n# 2. Prueba con un PDF real de tu ordenador.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="pypdf permite leer, escribir y manipular archivos PDF.",
            type="interactive"
        ),
        Lesson(
            id=95,
            title="PDF a Imágenes",
            content='Estudia el siguiente código: PDF a Imágenes',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Conversión real de PDF a Imagen\n# REQUISITO: pip install pdf2image\n# REQUISITO: Poppler instalado en el sistema (apt-get install poppler-utils)\n\nimport os\n\ntry:\n    from pdf2image import convert_from_path\n    HAS_LIB = True\nexcept ImportError:\n    HAS_LIB = False\n    print("Librería pdf2image no encontrada.")\n\nif HAS_LIB and os.path.exists("demo.pdf"):\n    print("Convirtiendo demo.pdf a imágenes...")\n    try:\n        images = convert_from_path("demo.pdf")\n        \n        for i, image in enumerate(images):\n            image_name = f"pagina_{i+1}.jpg"\n            image.save(image_name, "JPEG")\n            print(f"Guardada: {image_name}")\n            \n    except Exception as e:\n        print(f"Error (posiblemente falta Poppler): {e}")\nelse:\n    print("Saltando conversión (falta librería o archivo PDF).")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Este ejercicio requiere dependencias del sistema (Poppler).\n# 2. Es ideal para ejecutar en tu máquina local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="pdf2image convierte páginas de PDF en objetos de imagen PIL.",
            type="interactive"
        ),
        Lesson(
            id=96,
            title="Validador Regex",
            content='Estudia el siguiente código: Validador Regex',
            example_code='#!/usr/bin/python\n# pip install regex\nimport re\n\nprint("Iniciando Validador Regex...")\n\ndef validate_phone_number():\n    phone = "123-456-7890"\n    pattern = r"\\d{3}-\\d{3}-\\d{4}"\n    if re.match(pattern, phone):\n        print(f"Teléfono {phone} es válido")\n    else:\n        print(f"Teléfono {phone} es inválido")\n\ndef validate_username():\n    user = "User_123"\n    pattern = r"^[a-zA-Z0-9_]+$"\n    if re.match(pattern, user):\n        print(f"Usuario {user} es válido")\n    else:\n        print(f"Usuario {user} es inválido")\n\n# Ejecutar validaciones\nvalidate_phone_number()\nvalidate_username()\nprint("Validación completa.")\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=97,
            title="Renombrar Archivos Masivamente",
            content='Estudia el siguiente código: Renombrar Archivos Masivamente',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Script real para renombrar archivos\nimport os\nimport shutil\n\n# Configuración\ndir_objetivo = "fotos_viaje_test"\n\n# 1. Preparación: Crear directorio y archivos de prueba\nif not os.path.exists(dir_objetivo):\n    os.makedirs(dir_objetivo)\n    # Crear archivos dummy\n    open(f"{dir_objetivo}/101_playa.jpg", "w").close()\n    open(f"{dir_objetivo}/102_montana.jpg", "w").close()\n    open(f"{dir_objetivo}/103_cena.jpg", "w").close()\n    print(f"Archivos creados en {dir_objetivo}")\n\n# 2. Renombrado Real\nprint("\\nIniciando renombrado...")\narchivos = os.listdir(dir_objetivo)\n\nfor nombre_archivo in archivos:\n    ruta_completa = os.path.join(dir_objetivo, nombre_archivo)\n    \n    if os.path.isfile(ruta_completa):\n        # Lógica: Eliminar dígitos y guiones bajos al inicio\n        nuevo_nombre = "".join([c for c in nombre_archivo if not c.isdigit()]).lstrip("_")\n        \n        nueva_ruta = os.path.join(dir_objetivo, nuevo_nombre)\n        \n        # Renombrar\n        os.rename(ruta_completa, nueva_ruta)\n        print(f"Renombrado: {nombre_archivo} -> {nuevo_nombre}")\n\nprint("\\nVerificando resultados:")\nprint(os.listdir(dir_objetivo))\n\n# Limpieza (opcional)\n# shutil.rmtree(dir_objetivo)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código. Verás que realmente crea y renombra archivos.\n# 2. Modifica la lógica para añadir un prefijo "Vacaciones_" a todos.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="os.rename(origen, destino) es la función clave.",
            type="interactive"
        ),
        Lesson(
            id=98,
            title="Información del Sistema",
            content='Estudia el siguiente código: Información del Sistema',
            example_code='#!/usr/bin/python\nimport platform\nimport sys\nimport os\nimport socket\nimport time\n\n# Este script está probado en MacOS y funcionó bien. Debería funcionar en Linux también.\n\nunumber = os.getuid()\npnumber = os.getpid()\nwhere   = os.getcwd()\nnow     = time.time()\nmeans   = time.ctime(now)\n\nprint ("Número de usuario",unumber)\nprint ("ID de proceso",pnumber)\nprint ("Directorio actual",where)\n\nprint ("Nombre: " +socket.gethostname( ))\nprint ("Plataforma del sistema: "+sys.platform)\nprint ("Nodo " +platform.node())\nprint ("Plataforma: "+platform.platform())\nprint ("SO del sistema: "+platform.system())\nprint ("Release: " +platform.release())\nprint ("Versión: " +platform.version())\nprint ("Versión de Python: " +platform.python_version())\n\n# mostrando arquitectura de la plataforma\nprint(\'Arquitectura de la plataforma:\', platform.architecture())\n# mostrando procesador de la plataforma\nprint(\'Procesador de la plataforma:\', platform.processor())\n# mostrando tipo de máquina\nprint(\'Tipo de máquina:\', platform.machine())\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=99,
            title="Recordatorio de Descanso",
            content='Estudia el siguiente código: Recordatorio de Descanso',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Recordatorio real usando webbrowser\nimport time\nimport webbrowser\n\nprint("Iniciando monitor de descansos...")\nprint("Para la demo, esperaremos solo 3 segundos.")\n\n# Esperar (simulando trabajo)\ntime.sleep(3)\n\nprint("¡Hora del descanso!")\nurl = "https://www.google.com/search?q=ejercicios+de+estiramiento"\n\n# Abrir navegador real\n# Nota: Esto intentará abrir un navegador en el servidor si se ejecuta aquí.\n# En tu máquina local, abrirá tu Chrome/Firefox.\ntry:\n    webbrowser.open(url)\n    print(f"Se ha abierto el navegador en: {url}")\nexcept Exception as e:\n    print(f"No se pudo abrir el navegador: {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta este código en tu IDE local.\n# 2. Verás que realmente abre tu navegador web.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="webbrowser es una librería estándar de Python.",
            type="interactive"
        ),
        Lesson(
            id=100,
            title="Validador de Contraseñas",
            content='Estudia el siguiente código: Validador de Contraseñas',
            example_code='#!/usr/bin/python\nimport re\n\n# Criterios de Contraseña\n# 1. Debe contener alfanuméricos\n# 2. Al menos una Letra Mayúscula\n# 3. Al menos una letra minúscula\n# 4. 8-20 caracteres\n# 5. al menos un caracter especial !@#$%^&*_\n# 6. Sin espacios en blanco por favor\n\npasswords = [\'JassiSidhu\', \'Jassi Sidhu0$\',\'JassiSidhu0$\', \'Jalantu_123*\', \'12Falcon#\', \'Sh0rt5!\',\'Sh0rt5!89***^AWS+\', \'short\']\n\n# Usando Expresiones Regulares\npattern = \'^((?=.*\\\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_])(?=.*[\\\\S])[0-9a-zA-Z!@#$%^&*_]{8,20})$\'\nfor password in passwords:\n    print(f"Probando: {password}")\n    result = re.match(pattern,password)\n    if result:\n        print("  -> Contraseña Aceptada")\n    else:\n        print("  -> Contraseña Denegada")\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=101,
            title="Duración de Video",
            content='Estudia el siguiente código: Duración de Video',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Cálculo real de duración de video usando moviepy\n# REQUISITO: pip install moviepy\n\nimport os\n\ntry:\n    from moviepy.editor import VideoFileClip\n    HAS_MOVIEPY = True\nexcept ImportError:\n    HAS_MOVIEPY = False\n    print("Instala moviepy para analizar videos reales.")\n\ndef analizar_video(ruta_video):\n    if not HAS_MOVIEPY:\n        return\n    \n    if not os.path.exists(ruta_video):\n        print(f"Video no encontrado: {ruta_video}")\n        return\n\n    try:\n        clip = VideoFileClip(ruta_video)\n        duracion = clip.duration\n        print(f"Video: {ruta_video}")\n        print(f"Duración: {duracion:.2f} segundos")\n        print(f"Resolución: {clip.size}")\n        clip.close()\n    except Exception as e:\n        print(f"Error al leer video: {e}")\n\n# Demo: Crear un archivo dummy para que no falle la lógica de archivo\nif not os.path.exists("demo.mp4"):\n    print("No hay video demo.mp4. Si tuvieras uno, lo analizaríamos así:")\n    print("analizar_video(\'demo.mp4\')")\nelse:\n    analizar_video("demo.mp4")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Instala moviepy: pip install moviepy\n# 2. Coloca un archivo .mp4 en la carpeta y cambia el nombre en el código.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="MoviePy es una potente librería para edición de video.",
            type="interactive"
        ),
    ]
)
