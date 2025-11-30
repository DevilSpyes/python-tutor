from data.exercises import Module, Lesson

MODULE = Module(
    id=5,
    title="Módulo 05: Ciberseguridad y Criptografía",
    lessons=[
        Lesson(
            id=102,
            title="Criptografía Básica",
            content='Estudia el siguiente código: Criptografía Básica',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Criptografía Básica con Fernet\n# REQUISITO: pip install cryptography\n\nfrom cryptography.fernet import Fernet\n\nkey = Fernet.generate_key() \ncipher_suite = Fernet(key) \nmessage = "Este es un mensaje secreto para un grupo secreto. No para crackers, pero quizás para Criptoanalistas!.".encode()\n\ncipher_text = cipher_suite.encrypt(message) \nprint(\'El texto cifrado es: \' + str(cipher_text))\n\nplain_text = cipher_suite.decrypt(cipher_text)\nprint(\'Aquí está el texto plano:\' + str(plain_text))\n\nprint(\'\\nComprobando si el texto descifrado es igual a nuestro mensaje o no\')\n\nif plain_text == message: print("Sí, ambos son iguales\\n") \n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=103,
            title="Hashing de Contraseñas",
            content='Estudia el siguiente código: Hashing de Contraseñas',
            example_code='#!/usr/bin/python\n# Hashing de Contraseñas con hashlib\n# Aprende cómo se almacenan las contraseñas de forma segura.\n\nimport hashlib\n\npassword = "MiPasswordSeguro123"\nprint(f"Contraseña original: {password}")\n\n# 1. MD5 (Inseguro, rápido)\nmd5_hash = hashlib.md5(password.encode()).hexdigest()\nprint(f"MD5:    {md5_hash}")\n\n# 2. SHA-256 (Estándar actual)\nsha256_hash = hashlib.sha256(password.encode()).hexdigest()\nprint(f"SHA256: {sha256_hash}")\n\n# 3. Salted Hash (Más seguro)\n# Añadimos un valor aleatorio para evitar ataques de Rainbow Table\nsalt = "s4lT_r4nd0m"\nsalted_password = password + salt\nsalted_hash = hashlib.sha256(salted_password.encode()).hexdigest()\nprint(f"Salted: {salted_hash} (Salt: {salt})")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Cambia la contraseña y observa cómo cambian los hashes completamente (Efecto avalancha).\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=104,
            title="Cracking de Contraseñas (Hash)",
            content='Estudia el siguiente código: Cracking de Contraseñas (Hash)',
            example_code='#!/usr/bin/python\n# Cracking de Contraseñas (Ataque de Diccionario/Fuerza Bruta)\n# En un escenario real, el atacante obtiene el HASH de la contraseña, no la contraseña en texto plano.\n\nimport hashlib\nimport time\n\n# 1. El Hash robado (SHA-256 de un PIN de 4 dígitos)\n# Supongamos que obtuvimos esto de una base de datos filtrada.\n# (El hash corresponde a "4829")\nTARGET_HASH = "a2c4e6f323977e58455793f20e547622995a15a3038631665441655765566143"\n\nprint("--- Iniciando Cracking de Hash SHA-256 ---")\nprint(f"Objetivo: Encontrar el PIN que genera el hash: {TARGET_HASH[:10]}...")\n\nstart_time = time.time()\nfound = False\n\n# 2. Ataque de Fuerza Bruta (Espacio de claves: 0000-9999)\nfor i in range(10000):\n    # Generar candidato (ej. "0005")\n    pin_candidate = f"{i:04d}"\n    \n    # Calcular hash del candidato\n    candidate_hash = hashlib.sha256(pin_candidate.encode()).hexdigest()\n    \n    # Comparar\n    if candidate_hash == TARGET_HASH:\n        end_time = time.time()\n        print(f"\\n[¡ÉXITO!] Contraseña encontrada: {pin_candidate}")\n        print(f"Hash verificado: {candidate_hash}")\n        print(f"Tiempo: {end_time - start_time:.4f} segundos")\n        found = True\n        break\n    \n    if i % 2000 == 0:\n        print(f"Probando... {pin_candidate} -> {candidate_hash[:10]}...")\n\nif not found:\n    print("\\n[FALLO] No se encontró la contraseña en el rango probado.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Genera un nuevo hash de otro PIN en el ejercicio anterior y actualiza TARGET_HASH aquí para intentar crackearlo.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Los hackers comparan hashes calculados con hashes robados.",
            type="interactive"
        ),
        Lesson(
            id=105,
            title="Inyección SQL (Demo SQLite)",
            content='Estudia el siguiente código: Inyección SQL (Demo SQLite)',
            example_code='#!/usr/bin/python\n# Demostración de Inyección SQL usando SQLite en memoria\n\nimport sqlite3\n\n# Configuración de la Base de Datos\nconn = sqlite3.connect(":memory:")\ncursor = conn.cursor()\ncursor.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")\ncursor.execute("INSERT INTO users VALUES (1, \'admin\', \'admin123\')")\ncursor.execute("INSERT INTO users VALUES (2, \'user\', \'pass\')")\n\ndef login_vulnerable(user, pwd):\n    print(f"\\n[Intento de Login] User: {user} | Pass: {pwd}")\n    # VULNERABLE: Concatenación directa de strings\n    query = f"SELECT * FROM users WHERE username = \'{user}\' AND password = \'{pwd}\'"\n    print(f"[QUERY] {query}")\n    \n    try:\n        cursor.execute(query)\n        result = cursor.fetchone()\n        if result:\n            print(f"[RESULTADO] ¡Login Exitoso! Bienvenido {result[1]}")\n        else:\n            print("[RESULTADO] Acceso Denegado")\n    except Exception as e:\n        print(f"[ERROR SQL] {e}")\n\n# 1. Login Normal\nlogin_vulnerable("admin", "admin123")\n\n# 2. Login Fallido\nlogin_vulnerable("admin", "wrongpass")\n\n# 3. ATAQUE DE INYECCIÓN SQL\n# Usamos \' OR \'1\'=\'1 para hacer la condición siempre verdadera\nlogin_vulnerable("admin\' OR \'1\'=\'1", "basura")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código para ver cómo funciona el ataque.\n# 2. Intenta inyectar para loguearte como el usuario \'user\'.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=106,
            title="Detector de Phishing (URL)",
            content='Estudia el siguiente código: Detector de Phishing (URL)',
            example_code='#!/usr/bin/python\n# Analizador de URLs para detectar Phishing\n\nimport re\n\ndef analizar_url(url):\n    score = 0\n    razones = []\n    \n    # 1. Longitud excesiva\n    if len(url) > 75:\n        score += 10\n        razones.append("URL muy larga")\n        \n    # 2. Uso de dirección IP\n    ip_regex = r"\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}"\n    if re.search(ip_regex, url):\n        score += 20\n        razones.append("Usa dirección IP en lugar de dominio")\n        \n    # 3. Uso de @ para ofuscar\n    if "@" in url:\n        score += 15\n        razones.append("Contiene \'@\' (posible redirección)")\n        \n    # 4. Palabras clave sospechosas\n    sospechosas = ["secure", "account", "update", "login", "bank"]\n    for s in sospechosas:\n        if s in url and "https" not in url:\n            score += 5\n            razones.append(f"Palabra clave \'{s}\' en sitio no seguro")\n            \n    return score, razones\n\nurls = [\n    "https://www.google.com",\n    "http://192.168.1.1/login.php",\n    "http://secure-bank-update.com.badsite.org/login",\n    "https://google.com@malicious.com/file"\n]\n\nprint("--- Detector de Phishing ---")\nfor url in urls:\n    riesgo, detalles = analizar_url(url)\n    print(f"\\nURL: {url}")\n    print(f"Riesgo: {riesgo}%")\n    if detalles:\n        print(f"Alertas: {detalles}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código.\n# 2. Añade más URLs para probar el detector.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=107,
            title="Info de Cabeceras HTTP",
            content='Estudia el siguiente código: Info de Cabeceras HTTP',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Info de Cabeceras HTTP\n# REQUISITO: pip install requests validators colorama\n\nimport requests\nimport sys\nimport validators\nfrom colorama import init, Fore, Back, Style\n\ninit(autoreset=True)\n\n# --- CORRECCIÓN PARA EJECUCIÓN WEB ---\nif len(sys.argv) < 2:\n    print(Fore.YELLOW + "No se proporcionó URL. Usando por defecto: https://www.python.org")\n    sys.argv.append("https://www.python.org")\n# --------------------------\n\nurl = sys.argv[1]\n\nif validators.url(url):\n    try:\n        print(f"Obteniendo cabeceras para: {url}")\n        url_request = requests.get(url)\n\n        print(Fore.MAGENTA + Style.BRIGHT + "\\nCabeceras de Petición")\n        for req_header, value in url_request.request.headers.items():\n            print(f"{req_header}: {value}")\n            \n        print(Fore.CYAN + Style.BRIGHT + "\\nCabeceras de Respuesta")\n        for resp_header, value in url_request.headers.items():\n            print(f"{resp_header}: {value}")\n            \n        print(Fore.GREEN + Style.DIM + "\\n\\n====== Hecho ====== \\n")\n    except Exception as e:\n        print(f"Error: {e}")\nelse:\n    print("No es una url válida")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=108,
            title="Cabeceras de Seguridad",
            content='Estudia el siguiente código: Cabeceras de Seguridad',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Cabeceras de Seguridad\n# REQUISITO: pip install requests validators colorama\n\nimport requests\nimport sys\nimport validators\nfrom colorama import init, Fore, Back, Style\n\ninit(autoreset=True)\n\n# --- CORRECCIÓN PARA EJECUCIÓN WEB ---\nif len(sys.argv) < 2:\n    print(Fore.YELLOW + "No se proporcionó URL. Usando por defecto: https://www.python.org")\n    sys.argv.append("https://www.python.org")\n# --------------------------\n\ntry:\n    url = sys.argv[1]\n    if(validators.url(url)):\n        user_agent = \'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36\'\n        headers = {\'User-Agent\': user_agent}\n\n        session = requests.Session()\n        url_request = session.get(url, headers = headers)\n\n        print("Imprimiendo cabeceras de respuesta de url: " + Fore.GREEN + Style.BRIGHT + url )\n        print("Método de Petición: {}".format(url_request.request.method))\n\n        response_security_headers = [\'Server\', \'Content-Type\', \'Via\', \'X-Frame-Options\',\'X-Powered-By\', \'Strict-Transport-Security\', \n                            \'X-Content-Type-Options\', \'X-XSS-Protection\', \'X-Permitted-Cross-Domain-Policies\', \'Set-Cookie\', \'Cache-Control\',\n                            \'Transfer-Encoding\', \'Access-Control-Allow-Methods\', \'Access-Control-Allow-Origin\', \'Content-Security-Policy\', \'Referrer-Policy\']\n        for header in response_security_headers:\n            try:\n                result = url_request.headers[header]\n                print(\'%s: %s\' % (header, result))\n            except KeyError:\n                print (header + \': \' + Fore.RED + Style.BRIGHT + \'No encontrado\')\n\n        print(Fore.GREEN + Style.DIM + "\\n\\n====== Hecho ====== \\n")\n    else:\n        print("No es una url válida")\nexcept Exception as e:\n    print(Fore.MAGENTA + Style.BRIGHT + f"¡Algo salió mal! {e}")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=109,
            title="Escáner de Puertos (Socket)",
            content='Estudia el siguiente código: Escáner de Puertos (Socket)',
            example_code='#!/usr/bin/python\n# --- IMPORTANTE: EJECUCIÓN LOCAL REQUERIDA ---\n# Este ejercicio requiere librerías externas o generar archivos.\n# Por favor, ejecútalo en tu IDE local (VS Code, PyCharm, etc).\n# -----------------------------------------------------\n# Escáner de Puertos Simple usando Sockets\n# Escanea puertos comunes en localhost.\n\nimport socket\nimport sys\n\ntarget = "127.0.0.1" # Localhost\nports = [21, 22, 80, 443, 8000, 8080]\n\nprint(f"--- Escaneando {target} ---")\n\nfor port in ports:\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.settimeout(0.5)\n    \n    # Intentar conectar\n    result = s.connect_ex((target, port))\n    \n    if result == 0:\n        print(f"Puerto {port}: ABIERTO")\n    else:\n        print(f"Puerto {port}: CERRADO")\n        \n    s.close()\n\nprint("\\nEscaneo completado.")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código en tu IDE local.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),    ]
)
