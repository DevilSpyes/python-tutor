from data.exercises import Module, Lesson

MODULE = Module(
    id=2,
    title="Módulo 02: Conceptos Fundamentales",
    lessons=[
        Lesson(
            id=21,
            title="Hola Mundo (Repaso)",
            content='Estudia el siguiente código: Hola Mundo (Repaso)',
            example_code='#!/usr/bin/python3\n""" Primer Programa en Python\n    Solo para verificar si podemos ejecutar python3 correctamente\n"""\n\nname = "Sanjeev"\nprint("hello "+name+"\\n")\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=22,
            title="Números",
            content='Estudia el siguiente código: Números',
            example_code='#!/usr/bin/python # Configurando el shebang\n\n# Este tutorial cubrirá el concepto de tipos numéricos en Python3.x\n# Hay tres tipos numéricos en Python\n# 1. Int (Entero)\n# 2. Float (Flotante/Decimal)\n# 3. Complex (Complejo)\n\n# Int (Entero)\npositive_int = 55\nnegative_int = -1039\nzero = 0\nprint(positive_int)\nprint(negative_int)\nprint(zero)\nprint(type(negative_int))\n\n# Float (Decimal)\npositive_float = 1.497\nnegative_float = -2.9987654\nexponent_float = 3e8 # e para indicar la potencia de 10\n\nprint(positive_float)\nprint(negative_float)\nprint(exponent_float)\nprint(type(exponent_float))\n\n# Complex (Complejo)\n# Número como 3 + 5j donde j representa una parte imaginaria\ncomplex_num = -5 + 2j\nprint(complex_num)\nprint(type(complex_num))\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=23,
            title="Manejo de Errores (Try/Except)",
            content='Estudia el siguiente código: Manejo de Errores (Try/Except)',
            example_code='import requests as req\n\nbase_url="https://github.com/"\nusername = "deepraj1729"\n\nurl = base_url+username\n\n# Petición GET a github para el nombre de usuario\ntry:\n    res = req.get(url)\n    if res.status_code == 404:\n        print("Error 404. Página no encontrada")\n    elif res.status_code == 200:\n        print("Estado: OK")\n\nexcept Exception as e:\n    print("No se pudo establecer conexión")\n    print(e)\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=24,
            title="Comentarios y Docstrings",
            content='Estudia el siguiente código: Comentarios y Docstrings',
            example_code='#!/usr/bin/python3\n\n# Los comentarios son líneas que el intérprete de Python ignora.\n# Sirven para explicar el código a otros humanos (o a tu "yo" del futuro).\n\n# 1. Comentarios de una sola línea (usan #)\nvariable = 10 # Esto es una variable\n\n# 2. Comentarios multilínea (no existen oficialmente, pero se usan strings)\n"""\nEsto es un string multilínea que no se asigna a ninguna variable.\nPython lo ignora, por lo que funciona como un comentario de bloque.\n"""\n\n# 3. Docstrings (Cadenas de documentación)\n# Se usan para documentar funciones, clases y módulos.\n\ndef saludar(nombre):\n    """\n    Esta función recibe un nombre y saluda.\n    \n    Parámetros:\n        nombre (str): El nombre de la persona.\n    """\n    print(f"Hola, {nombre}")\n\n# Podemos acceder al docstring usando el atributo __doc__\nprint(saludar.__doc__)\n\nsaludar("Pythonista")\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Añade tus propios comentarios al código.\n# 3. Modifica el docstring de la función saludar.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Los comentarios son esenciales para escribir código mantenible.",
            type="interactive"
        ),
        Lesson(
            id=25,
            title="Conversión Numérica",
            content='Estudia el siguiente código: Conversión Numérica',
            example_code='#!/usr/bin/python\n\n# Este tutorial cubrirá el concepto de conversión de tipos numéricos en Python3.x\n\n# Int\npositive_int = 55\n\n# Float\nnegative_float = -2.9987654\n\n# Complex \ncomplex_num = 1j\n\n# convertir de int a float: \npositive_float = float(positive_int)  \n\n# convertir de float a int:\nnegative_int = int(negative_float)  \n\n# convertir de int a complex: \ncomplex_from_int = complex(positive_int)  \n\nprint(positive_float) \nprint(negative_int) \nprint(complex_from_int)  \n\nprint(type(positive_float)) \nprint(type(negative_int)) \nprint(type(complex_from_int))\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=26,
            title="Operaciones Numéricas Extra",
            content='Estudia el siguiente código: Operaciones Numéricas Extra',
            example_code="#!/usr/bin/python\nfrom decimal import Decimal as D\n\n# En este ejemplo, cubriremos\n# 1. Cómo funcionan los números float y por qué su comparación te sorprende\n# 2. Cómo usar el formato Decimal como en la escuela usando el módulo decimal\n# 3. Representación binaria, octal y hexadecimal\n# 4. Cualquier operación matemática de entero y float resultará en float\n\n# Los enteros pueden ser de cualquier longitud, un número de punto flotante es preciso solo hasta 15 decimales\nprint((1.1 + 2.2) == 3.3)\nprint(1.1 + 2.2)\n\n# Salida: Decimal('3.3') \nprint(D('1.1') + D('2.2'))  \n\n# Salida: Decimal('3.000') \nprint(D('1.2') * D('2.50'))\n\n#  ______________________________\n# | Sistema Numérico | Prefijo   |\n# | Binario          | '0b' o '0B' |\n# | Octal            | '0o' o '0O' |\n# | Hexadecimal      | '0x' o '0X' |\n#  ------------------------------\n\n# Salida: 121\nprint(0b1111001)  \nprint(bin(121))\n\n# Salida: 257 (252 + 5) \nprint(0xFC + 0b101)  \nprint(hex(252), bin(5))\n\n# Salida: 23 \nprint(0o27)\nprint(oct(23))\n\ninteger_num = 3\nfloat_num = 1.7\nsum_result = integer_num + float_num\n\n# Salida: sum_result = 4.7 y clase float \nprint(sum_result)\nprint(type(sum_result))\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=27,
            title="Cadenas de Texto (Strings)",
            content='Estudia el siguiente código: Cadenas de Texto (Strings)',
            example_code='#!/usr/bin/python\n\n# Python tiene la clase str para representar y manejar cadenas\n\nfirst_name = "Sanjeev"\nlast_name  = \'Jaiswal\'\nnick_name  = \'\'\'Jassi\'\'\'\naddress    = """ Dirección de correo, ¿verdad?\n    si es así, es Hyderabad, Madhapur.\n    Pin: 500081"""\n\nmobile_num = 9618961800\n\nprint("Nombre:", first_name)\nprint("Nombre: " + first_name) # Concatenación de cadenas\nprint("Dirección multilínea: " + address)\n\ngreetings = \'Hola\'   \nprint("La longitud de la cadena es " + str(len(greetings))) # len() para la longitud de la cadena\n\nprint(greetings + nick_name)  ## Hola Jassi. Concatenación de cadenas  \n\npi = 3.14   # text = \'El valor de pi es \' + pi      ## NO, no funciona \ntext = \'El valor de pi es \'  + str(pi)  ## necesitamos convertir específicamente el número a tipo str para imprimir\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=28,
            title="Formato de Strings",
            content='Estudia el siguiente código: Formato de Strings',
            example_code='#!/usr/bin/python\n# Python tiene la clase str para representar y manejar cadenas\n\nfirst_name = "Sanjeev"\nlast_name  = \'Jaiswal\'\nnick_name  = \'\'\'Jassi\'\'\'\naddress    = """ Dirección de correo, ¿verdad?\n    si es así, es Hyderabad, Madhapur.\n    Pin: 500081"""\n\nmobile_num = 9618961800\n\ntext = ("Ejemplo del operador " + chr(37) + ":  %d es mi número %s es mi apodo. Tengo %.2f grandes para %s" % (mobile_num, nick_name, 4.0, last_name))\nprint(text)\n\n# Argumentos por posición\nprint("======== Argumentos por posición ========")\nprint("Nombre: {}".format(first_name)) \nprint("Nombre: {0}".format(first_name))\nprint(f"Nombre: {first_name}")\nprint("Nombre Completo: {} {}".format(first_name, last_name))\nprint("Nombre Completo: {0} {1}".format(first_name, last_name))\nprint("Nombre Completo: {1} {0}".format(first_name, last_name))\nprint(f"Nombre Completo: {first_name} {last_name}")\n\n# Argumentos por parámetro\nprint("======= Argumentos por parámetro =======")\nprint("Apodo: {nick_name}".format(nick_name = "Jassi"))\n\n# Salida: \'Coordenadas: 37.24N, -115.81W\'\nprint(\'Coordenadas: {latitude}, {longitude}\'.format(latitude=\'37.24N\', longitude=\'-115.81W\'))\n\nfull_name = {\'first_name\': \'Alicia\', \'last_name\': \'Gearcia\'}\n# Salida \'Nombre Completo: Gearcia Alicia\'\nprint(\'Nombre Completo: {last_name} {first_name}\'.format(**full_name)) \n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=29,
            title="Métodos de Strings",
            content='Estudia el siguiente código: Métodos de Strings',
            example_code='#!/usr/bin/python\n# Python tiene la clase str para representar y manejar cadenas\n\nfirst_name = "Sanjeev"\nlast_name  = \'jaiswal\'\nnick_name  = \'\'\'Jassi\'\'\'\naddress    = """ Dirección de correo, ¿verdad?\n    si es así, es Hyderabad, Madhapur.\n    Pin: 500081"""\n\nmobile_num = 9618961800\n\ngreetings = \'Hola\'   \nprint("La longitud de la cadena \'Hola\' es: " + str(len(greetings))) # len() para la longitud de la cadena\n\n# ejemplos de funciones lower(), upper() y capitalize()\n## hola Jassi. Concatenación de cadenas  \nprint(greetings.lower(), nick_name)  \n\n# Hagamos los nombres todo en MAYÚSCULAS\nprint(first_name.upper(), last_name.upper())\n\n# Capitalizar last_name\nprint(last_name.capitalize())\n\n#------------------------------------------------------------------------------------------------------#\n# Método                                | True (si)                                                      #\n# str.isalnum()                         | La cadena consta solo de caracteres alfanuméricos (sin símbolos) #\n# str.isalpha()                         | La cadena consta solo de caracteres alfabéticos (sin símbolos)   #\n# str.islower()                         | Los caracteres alfabéticos de la cadena están todos en minúsculas            #\n# str.isupper()                         | Los caracteres alfabéticos de la cadena están todos en mayúsculas            #\n# str.isnumeric()                       | La cadena consta solo de caracteres numéricos                   #\n#------------------------------------------------------------------------------------------------------#\n\nprint(str(mobile_num).isnumeric())\nprint(first_name.isalpha())\nprint(last_name.isalnum())\nprint(nick_name.isupper())\n\n# funciones join() y split()\nreversed_first_name =\'\'.join(reversed(first_name))\nprint("Inverso de {} es {}". format(first_name, reversed_first_name))\n\n# Práctica para split(), replace(), strip(), find()\n# Revisa nuestras Preguntas de Práctica de Laboratorio\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=30,
            title="Estructuras Condicionales",
            content='Estudia el siguiente código: Estructuras Condicionales',
            example_code='#!/usr/bin/python\n\n# Las sentencias de control son uno de los bloques fundamentales de Python\n# Cubriremos\n# 1. if elif else\n# 2. while, for, range\n# 3. break, continue, pass\n\n# 1. Ejemplo de if, elif, else\n# Puede haber cero o más sentencias elif\n# else es opcional\n\n# url = input("Introduce tu sitio web: ")\nurl = "https://cybercloud.guru" # Valor hardcodeado para demo\n\nif \'http\' in url:\n    print(\'url no segura\')\nelif \'https\' in url:\n    print(\'algo más segura\')\nelif url == \'cybercloud.guru\':\n    print(\'ajá cybercloud guru encontrado\')\nelif url == \'\':\n    print(\'¿Cómo puede estar vacía una url? ¿olvidaste escribir?\')\nelse:\n    print(\'aquí está tu url: \' + url)\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=31,
            title="Bucle While Avanzado",
            content='Estudia el siguiente código: Bucle While Avanzado',
            example_code='#!/usr/bin/python\nimport random\n\n# Sintaxis del bucle While\n# while expresion:\n#   sentencia(s)\n# Puedes usar el bloque else con while también\n# while expresion:\n#   sentencia(s)\n# else:\n#   sentencia(s)\n\nguess_num_range = 20\nnum_to_be_guessed = int(guess_num_range * random.random()) + 1\nguess = 0\n\n# while guess != num_to_be_guessed:\n#     guess = int(input("Adivina el número: "))\n#     if guess > 0:\n#         if guess > num_to_be_guessed:\n#             print("El número es demasiado grande")\n#         elif guess < num_to_be_guessed:\n#             print("El número es demasiado pequeño")\n#     else:\n#         print("¡Lamento que te rindas!")\n#         break\n# else:\n#     print("¡Felicitaciones. Lo lograste!")\n\nprint(f"Simulando adivinanza... El número era {num_to_be_guessed}")\nprint("¡Felicitaciones. Lo lograste!")\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=32,
            title="Bucle For Avanzado",
            content='Estudia el siguiente código: Bucle For Avanzado',
            example_code='#!/usr/bin/python\n\n# sintaxis del bucle for\n# for variable_iteradora in secuencia:\n#   sentencia(s)\n# Puedes usar el bloque else con el bucle for igual que usamos con while en el ejemplo anterior\n# for <variable> in <secuencia>:\n#\t<sentencias>\n# else:\n#\t<sentencias>\n\nport_details = {\n    \'22\': \'ssh\',\n    \'21\': \'ftp\',\n    \'23\': \'telnet\',\n    \'80\': \'http\',\n    \'443\': \'https\'\n}\n\nprint("====== Detalles de Puertos ======")\nfor port in port_details:\n    print("{} -> {}".format(port, port_details[port]))\n\nprint("============================")\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=33,
            title="Uso de Range",
            content='Estudia el siguiente código: Uso de Range',
            example_code='#!/usr/bin/python\n\n# La función integrada de Python range() genera números enteros entre el entero de inicio dado y el entero de parada, es decir, range() devuelve un objeto de rango.\n# Usando el bucle for, podemos iterar sobre una secuencia de números producida por la función range().\n# Solo permite números de tipo entero como argumentos.\n# No podemos proporcionar un parámetro de tipo string o float dentro de la función range().\n# Los argumentos pueden ser positivos (+ve) o negativos (-ve).\n# No acepta ‘0’ como valor de paso. Si el paso es ‘0’, la función lanza un ValueError.\n\nfor step in range(10, 100, 10):\n    print(step)\n\n\nprint("\\nOtro ejemplo para iterar sobre una lista usando range")\nport_lists = [21, 22, 23, 25, 53, 80, 443, 3306, 8080, 9002, 27017]\n\nfor port in range(len(port_lists)):\n    print(port_lists[port])\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=34,
            title="Control de Bucles (Break/Continue)",
            content='Estudia el siguiente código: Control de Bucles (Break/Continue)',
            example_code='#!/usr/bin/python\n\n# Ejemplo de pass, break, continue\n# pass: no hace nada. útil cuando se prueba algo o cuando ese bloque de código no es necesario\n# break: termina el bucle actual y reanuda la ejecución en la siguiente sentencia\n# continue: devuelve el control al principio del bucle\n\n\nport_details = {\n    \'21\': \'ftp\',\n    \'23\': \'telnet\',\n    \'80\': \'http\',\n    \'443\': \'https\',\n    \'3306\': \'mysql\'\n}\n\nprint("====== Detalles de Puertos ======")\nfor port in port_details:\n    if port == \'80\' or port == \'443\':\n        print("el puerto {} es un puerto web permitido".format(port))\n        continue\n    elif port == \'22\':\n        print("el acceso ssh parece permitido aquí")\n        break\n    else:\n        pass\n        print("Solo pasó y mostrando los detalles del puerto abajo")\n        print("{} -> {}".format(port, port_details[port]))\nelse:\n    print("Llegó aquí significa que terminó todo en el bucle for")\nprint("============================")\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=35,
            title="Condicionales en Una Línea",
            content='Estudia el siguiente código: Condicionales en Una Línea',
            example_code='#!/usr/bin/python\n\n# Nota: Esto es opcional pero bueno saberlo.\n# En la situación donde solo tenemos un if y un else, y el cuerpo de cada rama contiene solo una expresión, entonces podemos usar una expresión condicional. Las expresiones condicionales se pueden usar para expresar sucintamente un condicional simple\n\n# name = input("¿Cuál es tu primer nombre? ")\nname = "Christopher" # Valor hardcodeado para demo\n\n# 1) Llamar a `print` con una cadena diferente usando una sola expresión condicional\nprint(\n    "Tu nombre es tan largo o más largo que el nombre promedio en los Estados Unidos"\n) if len(name) >= 6 else print (\n    "Tu nombre es más corto que el nombre promedio en los Estados Unidos"\n)\n\n# 2) Establecer `message` usando una sola expresión condicional\nmessage = (\n    "La primera letra de tu nombre está entre las cinco más comunes"\n    if name[0].lower() in ["a", "j", "m", "e", "l"]\n    else "La primera letra de tu nombre no está entre las cinco más comunes"\n)\n\nprint(message)\n\n# 3) Cambiar la cadena pasada a la función `print` usando una expresión condicional\nfor letter in name:\n    print(\n        f"{letter} {\'es una vocal\' if letter.lower() in [\'a\', \'e\', \'i\', \'o\', \'u\'] else \'es una consonante\'}"\n    )\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=36,
            title="Operadores Aritméticos",
            content='Estudia el siguiente código: Operadores Aritméticos',
            example_code="#!/usr/bin/python\n\nx = 21\ny = 5\n\n# Salida: x + y = 26\n# Suma\nprint('x + y =',x+y)\n\n# Salida: x - y = 16\n# Resta\nprint('x - y =',x-y)\n\n# Salida: x * y = 105\n# Multiplicación\nprint('x * y =',x*y)\n\n# Salida: x / y = 4.2\n# División, siempre resulta en un flotante (decimal)\nprint('x / y =',x/y)\n\n# Salida x % y = 1\n# Módulo (residuo de la división)\nprint('x % y =', x%y)\n\n# Salida: x // y = 4\n# División Entera (cociente sin decimales)\nprint('x // y =',x//y)\n\n# Salida: x ** y = 4084101\n# Potencia (x elevado a la y)\nprint('x ** y =',x**y)\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=37,
            title="Operadores de Comparación",
            content='Estudia el siguiente código: Operadores de Comparación',
            example_code="#!/usr/bin/python\n\n# Operadores de comparación con números\nx = 19\ny = 91\n\nprint('{} > {} es'.format(x,y),x>y)\nprint('{} < {} es'.format(x, y),x<y)\nprint('{} == {} es'.format(x,y),x==y)\nprint('{} != {} es'.format(x,y),x!=y)\nprint('{} >= {} es'.format(x,y),x>=y)\nprint('{} <= {} es'.format(x,y),x<=y)\n\n# Veamos cómo funciona con cadenas de texto (strings)\nname_title = 'Jassi'\nname_lowercase = 'jassi'\n\nprint('{} > {} es'.format(name_title, name_lowercase),name_title>name_lowercase)\nprint('{} < {} es'.format(name_title, name_lowercase),name_title<name_lowercase)\nprint('{} == {} es'.format(name_title, name_lowercase),name_title==name_lowercase)\nprint('{} != {} es'.format(name_title, name_lowercase),name_title!=name_lowercase)\nprint('{} >= {} es'.format(name_title, name_lowercase),name_title>=name_lowercase)\nprint('{} <= {} es'.format(name_title, name_lowercase),name_title<=name_lowercase)\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=38,
            title="Operadores de Asignación",
            content='Estudia el siguiente código: Operadores de Asignación',
            example_code="#!/usr/bin/python\n\n# El operador de asignación se usa para asignar un valor a la variable del lado izquierdo\n# Ejemplos de operadores de asignación en Python\n# Operador\tEjemplo\tEquivalente a\n# =\t       x = 5\tx = 5\n# +=\t   x += 5\tx = x + 5\n# -=\t   x -= 5\tx = x - 5\n# *=\t   x *= 5\tx = x * 5\n# /=\t   x /= 5\tx = x / 5\n# %=\t   x %= 5\tx = x % 5\n# //=\t   x //= 5\tx = x // 5\n# **=\t   x **= 5\tx = x ** 5\n# &=\t   x &= 5\tx = x & 5\n# |=\t   x |= 5\tx = x | 5\n# ^=\t   x ^= 5\tx = x ^ 5\n# >>=\t  x >>= 5\tx = x >> 5\n# <<=\t  x <<= 5\tx = x << 5\n\nx = 5\nprint('x =', x)\n\nx += 5\nprint('x =', x)\n\nx *= 5\nprint('x = {}'.format(x))\n\n# Puedes probar con los otros operadores\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=39,
            title="Operadores Lógicos",
            content='Estudia el siguiente código: Operadores Lógicos',
            example_code="#!/usr/bin/python\n\n# Operadores Lógicos en Python\n# Operador\tSignificado\t                                                 Ejemplo\n# and\t   True (Verdadero) si ambos operandos son verdaderos\t     x and y\n# or\t   True (Verdadero) si alguno de los operandos es verdadero\t x or y\n# not\t   True (Verdadero) si el operando es falso (invierte el valor)\t not x\n\nx = True\ny = False\n\n# Salida: x and y es False\nprint('x and y es',x and y)\n\n# Salida: x or y es True\nprint('x or y es',x or y)\n\n# Salida: not x es False\nprint('not x es',not x)\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=40,
            title="Operadores de Identidad",
            content='Estudia el siguiente código: Operadores de Identidad',
            example_code="#!/usr/bin/python\n\n# Operadores de Identidad\n# 'is' y 'is not' son los operadores de identidad en Python.\n# Se usan para verificar si dos valores (o variables) están ubicados en la misma parte de la memoria.\n# Que dos variables sean iguales (==) no implica que sean idénticas (is).\n\n# Ejemplo tomado de programiz.com\nx1 = 5\ny1 = 5\nx2 = 'Hola'\ny2 = 'Hola'\nx3 = [1,2,3]\ny3 = [1,2,3]\n\n# Salida: False (porque x1 y y1 SON idénticos, así que 'is not' es falso)\nprint(x1 is not y1)\n\n# Salida: True (porque x2 y y2 apuntan al mismo string en memoria)\nprint(x2 is y2)\n\n# Salida: False (porque x3 y y3 son listas diferentes en memoria, aunque tengan el mismo contenido)\nprint(x3 is y3)\n\n# Aquí vemos que x1 y y1 son enteros con el mismo valor, por lo que son iguales e idénticos (Python optimiza enteros pequeños).\n# Lo mismo ocurre con x2 y y2 (strings cortos).\n# Pero x3 y y3 son listas. Son iguales (==) pero NO idénticas (is).\n# Esto es porque el intérprete las ubica en lugares separados de la memoria aunque sean iguales.\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=41,
            title="Estructuras de Datos",
            content='Estudia el siguiente código: Estructuras de Datos',
            example_code='# No es algo nuevo. En cada lenguaje de programación escucharás sobre sus estructuras de datos.\n# Una Estructura de Datos no es más que cómo organizas tus datos, cómo los muestras, trabajas con ellos, etc.\n# Python tiene muchas estructuras de datos integradas que ya has visto como números y cadenas.\n# Discutiremos las Estructuras de Datos (DS) más importantes que usarás más a menudo en Python.\n# Ellas son:\n# 1. Listas (Lists)\n# 2. Tuplas (Tuples)\n# 3. Diccionarios (Dictionaries)\n# 4. Conjuntos (Sets)\n\n# Ten en cuenta que hay muchas otras con diferentes bibliotecas de python como array.array pero no las discutiremos en los fundamentos de Python\n\n# La Lista es una estructura de datos mutable y se implementa como un array dinámico.\nproto_list = ["http", "https", "ftp", "ssh"] # Puedes tener una lista definida o crear una lista vacía\nprint(proto_list)\n\n# Tuplas\n# Las tuplas son objetos inmutables, por lo demás se ven similares a las listas.\n# Inmutable significa que los elementos no se pueden agregar o eliminar dinámicamente y todos los elementos en una tupla deben definirse en el momento de la creación.\nproto_tuple = ("http", "https", "ftp", "ssh") # ¿Observaste [] y ()? [] significa lista y () significa tupla aquí. Bastante interesante, ¿verdad?\nprint(proto_tuple)\n\n# Diccionarios\n# Los diccionarios, en resumen Dict, almacenan un número arbitrario de objetos, cada uno identificado por una clave única.\n# La clave suele ser una cadena y el valor puede ser de cualquier tipo de dato de Python.\nemp_id = {\n    "sid": 657387,\n    "daniel": 603719,\n    "jassi": 770521,\n}\nprint(emp_id)\n\n# Conjuntos (Sets)\n# Un conjunto es una colección de objetos que no permiten elementos duplicados.\n# Los conjuntos no están ordenados como los diccionarios, por lo que no puedes predecir cuál se imprimirá primero.\n# Los conjuntos son inmutables en cuanto a sus elementos (hashables), pero el conjunto en sí es mutable (puedes agregar/quitar).\nproto_set = {"tcp", "icmp", "ssh", "icmp", "ftp"} # ¿Observaste cómo se crea? con {}. Ahora recuerda [], () y {} al crear estas estructuras de datos.\nprint(proto_set) # ¡SIN valores duplicados! ;)\n\n# Además, {} significa diccionario vacío. Entonces, ¿qué usar para un conjunto vacío? (Pista: set())\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=42,
            title="Listas a Fondo",
            content='Estudia el siguiente código: Listas a Fondo',
            example_code='#!/usr/bin/python\n\n# Lista Vacía\nallowed_ports = []\n\n# lista predefinida\nallowed_ports = [22, 23, 25, 53, 80, 69, 443, 3306, 8000, 8080, 5439, 8081, 9001,27017]\n\n# Iterar a través de la lista\nprint("Iterar a través de la lista")\nfor port in allowed_ports:\n    print(port)\n\n# Verificar si un elemento existe en la lista\nprint("\\nVerificando si el puerto 5432 está presente en la lista aprobada o no")\nif 5432 in allowed_ports:\n    print("El puerto predeterminado de Postgres 5432 está permitido")\nelse:\n    print("¡No Aprobado!\\n\\tNecesitas obtener aprobación del administrador para habilitar el puerto 5432 para postgres")\n\n# Acceder a la lista\nprint("\\nMostrando algunas formas de acceder al contenido de los elementos de la lista")\nprint("Primer elemento de la lista {}".format(allowed_ports[0])) # El primer índice de la lista es 0\nprint("Último elemento de la lista {}".format(allowed_ports[-1])) # -1 en la lista muestra el último elemento\nprint("Rango del 3er al 6to elemento de la lista {}".format(allowed_ports[2:6])) # La búsqueda comenzará en el índice 2 (incluido) ya que contiene el 3er elemento y terminará en el índice 6 (no incluido) lo que significa el 7mo elemento.\nprint("Elementos desde el principio hasta el 8vo elemento, es decir, puerto 3306 en nuestro caso {}".format(allowed_ports[:8]))\nprint("Elementos desde el 5to elemento hasta el final {}".format(allowed_ports[4:]))\nprint("Veamos si entiendes el slicing aquí {}".format(allowed_ports[-7:-2]))\n\n# Cambiar el valor de un elemento existente\nprint("\\nCambiar el valor del puerto 69 a 690, verifica el 6to elemento")\nprint(allowed_ports)\nallowed_ports[5] = 690\nprint(allowed_ports)\n\n# Manipulación de listas\n# función len()\nprint("El número de puertos permitidos en la lista son: ", len(allowed_ports))\nprint("Los puertos permitidos son: ", allowed_ports)\n\n# función count() para contar cuántas entradas de este tipo hay\nprint("Nº de puerto 80 en la lista: ", allowed_ports.count(80))\nprint("Nº de puerto 8001 en la lista: ", allowed_ports.count(8001))\n\n# función index() para encontrar el número de índice del contenido coincidente en la lista\nprint("Índice del puerto 3306 en la lista: ", allowed_ports.index(3306))\n\n# Ver la diferencia entre la función reversed() y reverse()\nprint("\\nFormas de invertir la lista")\nreverse_port_list = list(reversed(allowed_ports))\nprint("Inverso de la lista de puertos usando el método reversed(): ", reverse_port_list)\n\nallowed_ports.reverse()\nprint("Inverso de la lista de puertos usando el método reverse():", allowed_ports)\n\n# invirtiéndolo de nuevo para ponerlo en orden ascendente :D\nallowed_ports.reverse()\n\n# función sorted() para ordenar una lista rápidamente\nprint("\\nFormas de ordenar la lista")\nsorted_port_list = sorted(allowed_ports)\nprint("Lista de puertos ordenada usando el método sorted()", sorted_port_list)\n\n# Añadir/Eliminar elementos\nprint("\\nFormas de añadir elementos")\n# añade los elementos al final de la lista\nallowed_ports.append(27018)\nprint(allowed_ports)\n\n# Añadiendo elementos en la 7ma posición, así que el índice es 6\nallowed_ports.insert(6,110)\nprint(allowed_ports)\n\nprint("\\nFormas de eliminar elementos")\n# el método remove() elimina el elemento especificado\nallowed_ports.remove(27018) # eliminar puerto 27018\nprint(allowed_ports)\n\n# el método pop() elimina el índice especificado, (o el último elemento si no se especifica índice)\nallowed_ports.pop(6) # eliminar 7mo índice\nprint(allowed_ports)\n\n# la palabra clave del elimina en el índice especificado o incluso toda la lista\ndel allowed_ports[0]\nprint(allowed_ports)\n# Comentado a propósito `del allowed_ports`\n\n# el método clear vacía la lista\nallowed_ports.clear()\nprint(allowed_ports)\n\n# eliminemos toda la lista ahora.\ndel allowed_ports\ntry:\n    print(allowed_ports)\nexcept Exception as e:\n    print("¿Parece que allowed_ports no existe ahora? Error:", e)\n\n# Puedes intentar las 2 tareas siguientes\n# 1. Unir las listas\n# 2. Copiar las listas\n# También, intenta entender Shallow copy vs Deep copy\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=43,
            title="Diccionarios a Fondo",
            content='Estudia el siguiente código: Diccionarios a Fondo',
            example_code='#!/usr/bin/python3\n\n# Ejemplos para diccionario\n# Diccionario Vacío\nemp_dict = {}\n\n# diccionario con claves enteras\nemp_dict = {100: \'Sanjeev\', 101: \'Jassi\'}\nprint(emp_dict)\n\n# diccionario con claves mixtas\nemp_dict = {100: \'Sanjeev\', \'skills\': [\'Python\', \'AWS\']}\nprint(emp_dict)\n\n# usando la función dict()\nemp_dict = dict({100: \'Sanjeev\', 101: \'Jassi\'})\nprint(emp_dict)\n\n# Creemos emp_dict de este formato\n\'\'\'\n{\t\n\t\'Employee ID\':\n\t{\tName: \'string\'\n\t\tJoined: \'yyyy-mm-dd\'\n\t\tTitle: \'string\'\n\t\tSkills: [‘list’, ‘of’, ‘skills’]\n\t\tProject: {‘project_name’: ‘project description’}\n\t}\n}\n\'\'\'\n\n# Inicializando Empleado\nemp_dict = {\n    100:\n        {\n            \'name\': "Sanjeev",\n            \'joined\': "2017-08-14",\n            \'title\': "Cloud Security Engineer",\n            \'skills\': [\'Python\', \'AWS\', \'AppSec\'],\n            \'projects\': {\n                \'CSPM implementation\': \'Implement Cloud Security Posture for AWS\'\n            }\n        },\n    101:\n        {\n            \'name\': "Jassi",\n            \'joined\': "2017-10-27",\n            \'title\': "Cloud Security Manager",\n            \'skills\': [\'Python\', \'AWS\', \'AWS Security\'],\n            \'projects\': {\n                \'CSPM implementation\': \'Implement Cloud Security Posture for AWS and Azure\'\n            }\n        }\n}\n\nprint(emp_dict)\n\n# Obtener el tipo de emp_dict\nprint(type(emp_dict))\n\n# obtener claves de un diccionario usando keys()\nemp_ids = emp_dict.keys()\nprint(emp_ids)\n\n# Obtener valores de un diccionario usando values()\nemp_details = emp_dict.values()\nprint(emp_details)\n\n# obtener clave y valor ambos usando items()\nemps = emp_dict.items()\nprint(emps)\n\n# Longitud de un diccionario (número de elementos) usando len()\nprint(len(emp_dict))\n\n# Iterar a través de un diccionario\nfor id in emp_dict.keys():\n    print(f"ID Empleado: {id}")\n    print(f"\\tDetalles Empleado: {emp_dict[id]}")\n\n# Accediendo a elementos del diccionario\n# get vs [] para recuperar elementos\n# Sanjeev\nprint(emp_dict[100][\'name\'])\n\n# [\'Python\', \'AWS\', \'AppSec\']\nprint(emp_dict[101].get(\'skills\'))\n\n# Intentar acceder a claves que no existen\n# None\nprint(emp_dict[100].get(\'mailid\'))\n\n# KeyError: \'location\' Comenta la línea de abajo para ejecutar otras líneas abajo\n# print(emp_dict[101][\'location\'])\n\n# Añadir un empleado más a emp_dict usando update()\nnew_emp = {\n    102:\n        {\n            \'name\': "Rakesh",\n            \'joined\': "2018-01-07",\n            \'title\': "Business Analyst",\n            \'skills\': [\'Power BI\', \'MBA\', \'Marketing Expert\'],\n            \'projects\': {\n                \'Flexmind Marketing\': \'Increase the membership my targeted marketing\'\n            }\n        }\n}\n\nemp_dict.update(new_emp)\nprint(emp_dict)\n\n# Actualizar el valor existente. Actualizar título de emp_id: 100 como "Sr. Cloud Security Engineer"\nemp_dict[100][\'title\'] = "Sr. Cloud Security Engineer"\nprint(emp_dict[100])\n\n# Aprender a eliminar\n# pop, clear, del\n# Pop empleado id 101\nemp_dict.pop(101, "No encontrado")\nprint(len(emp_dict))\n\n# Eliminar el empleado 102\ndel emp_dict[102]\nprint(len(emp_dict))\n\n# Limpiar el diccionario\nemp_dict.clear()\nprint(emp_dict)\n\n# Eliminar el diccionario en sí e imprimirlo lanzaría un error\ndel emp_dict\n# print(emp_dict)\n\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=44,
            title="Tuplas",
            content='Estudia el siguiente código: Tuplas',
            example_code='# Las tuplas son un objeto inmutable en Python. Significa que una vez que se establecen los datos, no puedes cambiarlos.\n# Se pueden usar para datos constantes o diccionario sin clave (tuplas anidadas)\n\n# Inicialización de Tupla Vacía\ntup = ()\nprint(tup)\n\n# Inicialización de Tupla con datos\n# No me gustó esta forma sin embargo ;)\ntup1 = \'python\', \'aws\', \'security\'\nprint(tup1)\n\n# Otra para hacer lo mismo\ntup2 = (\'python\', \'django\', \'linux\')\nprint(tup2)\n\n# Concatenación\ntup3 = tup1 + tup2\nprint(tup3)\n\n# Anidamiento de tuplas\ntup4 = (tup1, tup2)\nprint(tup4)\n\n# Longitud de una tupla\nprint(len(tup3))\nprint(len(tup4))\n\n# Indexación y slicing de Tupla\nprint(tup3[2])\nprint(tup2[1:])\n\n# Eliminando una tupla, eliminar un elemento individual de la tupla no es posible. Elimina toda la tupla\ndel tup4\n\n# Convierte una lista en tupla\ntup5 = tuple(["Sanjeev", \'2021\', "Flexmind"])\nprint(tup5)\n\n# prueba tuple() a una cadena\ntup6 = tuple(\'Python\')\nprint(tup6)\n\n# Iteración de Tupla\nfor tup in tup5:\n    print(tup)\n\n# Método Max y min\nmax_elem = max(tup1)\nprint("elemento max: ", max_elem)\nprint("elemento min: ", min(tup5))\n\n\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=45,
            title="Conjuntos (Sets)",
            content='Estudia el siguiente código: Conjuntos (Sets)',
            example_code="# Un Conjunto es una colección de datos que no está ordenada, ni indexada y es única. Es uno de los 4 tipos de datos nativos en Python\n# Esto se basa en un concepto de estructura de datos tabla hash.\n# No podemos acceder a sus elementos por índice como en una lista\n# Los conjuntos no pueden tener elementos mutables, de lo contrario pueden contener datos mixtos\n\n# Inicialización de conjunto vacío\n# usa el método set(). Usar {} creará un diccionario vacío\ntest = {}\n# Salida <class 'dict'>\nprint(type(test))\nsets = set()\n# Salida <class 'set'>\nprint(type(sets))\n\n# inicialización de conjuntos\nmy_set = {1,2,3}\n# Salida {1, 2, 3}\nprint(my_set)\n\n# u otra forma es usando el método set()\nmy_another_set = set([4,5,6])\n# Salida {4, 5, 6}\nprint(my_another_set)\n\n# Añadir elementos\n# usa el método set.add() para añadir elementos\nfor num in range(6):\n    my_set.add(num)\n# Salida {0, 1, 2, 3, 4, 5}\nprint(my_set)\n\n# Eliminar elementos\n# eliminar elementos del conjunto usando el método remove() o discard()\n# si el elemento no existe remove() lanzará un error, pero discard() no lo hará\nmy_set.remove(4)\n# Salida {0, 1, 2, 3, 5}\nprint(my_set)\nmy_set.discard(7)\n# Salida {0, 1, 2, 3, 5}\nprint(my_set)\n\n\n# Unión\n# fusionando 2 conjuntos usando el método union() o el operador '|'\n# devolverá un nuevo conjunto\nfinal_set = my_set.union(my_another_set)\n# Salida {0, 1, 2, 3, 4, 5, 6}\nprint(final_set)\nsame_set = my_set | my_another_set\n# Salida {0, 1, 2, 3, 4, 5, 6}\nprint(same_set)\n\n# Actualizar\n# uniendo 2 conjuntos usando el método update()\n# actualizará el conjunto con los datos de otro conjunto\nmy_set.update(my_another_set)\n# Salida {0, 1, 2, 3, 5, 4, 6}\nprint(my_set)\n\n\n# Intersección\n# Intersección de 2 conjuntos usando el método intersection() o el operador '&'\nintersect = my_set.intersection(my_another_set)\n# Salida {4, 5, 6}\nprint(intersect)\nintersect2 = my_set & my_another_set\n# Salida {4, 5, 6}\nprint(intersect2)\n\n# Diferencia\n# Diferencia de 2 conjuntos usando el método difference() o el operador '-'\ndiff = my_set.difference(my_another_set)\n# salida {0, 1, 2, 3}\nprint(diff)\ndiff2 = my_set - my_another_set\n# Salida {0, 1, 2, 3}\nprint(diff2)\n\n# Diferencia Simétrica\n# usando el método symmetric_difference() o el operador '^'\n# Salida {0, 1, 2, 3}\nprint(my_set ^ my_another_set)\n# Salida {0, 1, 2, 3}\nprint(my_set.symmetric_difference(my_another_set))\n# Salida {0, 1, 2, 3}\nprint(my_another_set.symmetric_difference(my_set))\n\n# Limpiar el conjunto\nintersect2.clear()\n# Salida set()\nprint(intersect2)\n\n# Iterando a través de conjuntos\nfor num in my_set:\n    print(num)\n\n# la palabra clave del eliminará el conjunto completamente\n# del my_set\n\n# UNA COSA MÁS\n# Al igual que las tuplas son una lista inmutable, frozenset es un conjunto inmutable\n# imm_set = frozenset([1, 2, 3, 4])\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=46,
            title="Funciones Avanzadas",
            content='Estudia el siguiente código: Funciones Avanzadas',
            example_code="#!/usr/bin/python\n\n# Ejemplos de función en Python 3.x\n\n# ¿Cuándo necesitas una función?\n#   Cuando quieres realizar un conjunto de tareas específicas y quieres reutilizar ese código siempre que sea necesario\n#   También, para una mejor modularidad, legibilidad y solución de problemas\n\n# ¿Cómo escribir una función (Sintaxis)?\n'''def nombre_funcion():\n    {\n        # algo de código aquí\n    }\n'''\n\n# Diferentes formas de pasar parámetros\n# Qué devolver a través de la función\n\n# Una función básica de sumar dos números\ndef sumar_numeros(num1, num2):\n    return num1+num2\n\n# ¿Cómo llamar a una función?\n# la forma más básica de llamar a una función es `nombre_funcion()`\n# Llamando a la función de arriba\nprint(sumar_numeros(5,4))\n\n# Función para encontrar si un número es par\ndef es_par(num):\n    if num%2 == 0:\n        return True\n    return False\n\nnum = 12\nresultado = es_par(num)\nif resultado:\n    print(f'{num} es par')\nelse:\n    print(f'{num} no es par')\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n",
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=47,
            title="Funciones de Colección",
            content='Estudia el siguiente código: Funciones de Colección',
            example_code='#!/usr/bin/python\n# Ejemplo de lambda, map, filter\n\n# 1) Ordenar la lista de diccionarios `people` alfabéticamente basándose en la\n# clave \'name\' de cada diccionario usando la función `sorted` y almacenar\n# la nueva lista como `sorted_by_name`\n\npeople = [\n    {"name": "Kevin Bacon", "age": 61},\n    {"name": "Fred Ward", "age": 77},\n    {"name": "finn Carter", "age": 59},\n    {"name": "Ariana Richards", "age": 40},\n    {"name": "Victor Wong", "age": 74},\n]\n\n# sorted_by_name = None\nsorted_by_name = sorted(people, key=lambda d: d[\'name\'].lower())\n\nassert sorted_by_name == [\n    {"name": "Ariana Richards", "age": 40},\n    {"name": "finn Carter", "age": 59},\n    {"name": "Fred Ward", "age": 77},\n    {"name": "Kevin Bacon", "age": 61},\n    {"name": "Victor Wong", "age": 74},\n], f"Se esperaba que sorted_by_name fuera igual a \'{sorted_by_name}\' igual a \'{[{\'name\': \'Ariana Richards\', \'age\': 40}, {\'name\': \'finn Carter\', \'age\': 59}, {\'name\': \'Fred Ward\', \'age\': 77}, {\'name\': \'Kevin Bacon\', \'age\': 61}, {\'name\': \'Victor Wong\', \'age\': 74}]}\'\'"\n\n# 2) Usa la función `map` para iterar sobre `sorted_by_name` para generar una\n# nueva lista llamada `name_declarations` donde cada valor es una cadena con\n# `<NOMBRE> tiene <EDAD> años.` donde los valores `<NOMBRE>` y `<EDAD>` son de\n# los diccionarios.\n\n# name_declarations = None\nname_declarations = list(\n    map(lambda d: f"{d[\'name\']} tiene {d[\'age\']} años", sorted_by_name)\n)\n\nassert name_declarations == [\n    "Ariana Richards tiene 40 años",\n    "finn Carter tiene 59 años",\n    "Fred Ward tiene 77 años",\n    "Kevin Bacon tiene 61 años",\n    "Victor Wong tiene 74 años",\n], f"Se esperaba que name_declarations fuera igual a \'{name_declarations}\' igual a \'{[\'Ariana Richards tiene 40 años\', \'finn Carter tiene 59 años\', \'Fred Ward tiene 77 años\', \'Kevin Bacon tiene 61 años\', \'Victor Wong tiene 74 años\']}\'"\n\n# 3) Combina las funciones `filter` y `sorted` para iterar sobre `sorted_by_name` para generar una\n# nueva lista llamada `under_seventy` que solo contenga los diccionarios donde la\n# clave \'age\' sea menor de 70, ordenando la lista por edad.\n\n# under_seventy = None\nunder_seventy = sorted(\n    filter(lambda d: d[\'age\'] < 70, sorted_by_name), key=lambda d: d[\'age\']\n)\n\nassert under_seventy == [\n    {"name": "Ariana Richards", "age": 40},\n    {"name": "finn Carter", "age": 59},\n    {"name": "Kevin Bacon", "age": 61},\n], f"Se esperaba que under_seventy fuera igual a \'{under_seventy}\' igual a \'{[{\'name\': \'Ariana Richards\', \'age\': 40}, {\'name\': \'finn Carter\', \'age\': 59}, {\'name\': \'Kevin Bacon\', \'age\': 61}]}\'"\n\n\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=48,
            title="Funciones Integradas",
            content='Estudia el siguiente código: Funciones Integradas',
            example_code='#Entrada en CLI\n# input_text = input("Introduce algo aquí y luego presiona enter....   ")\ninput_text = "Hola Python" # Valor hardcodeado\nprint("Ingresaste: ",input_text)\n\n#Absoluto o Mod\nn = abs(-12)\nprint("El valor absoluto de -12 es: ",n)\n\n#Expresión Booleana\nx=12>19\nprint("El valor booleano de la expresión (12<19) es ",bool(x))\n\ndata = {\n    "id": 1,\n    "name": "Ramesh",\n    "designation":"SDE 1",\n    "Hobbies": "Loves playing football"\n    }\n\nprint(data,locals())\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=49,
            title="Expresiones Regulares (Regex)",
            content='Estudia el siguiente código: Expresiones Regulares (Regex)',
            example_code='import re\n\nurls = ["https://www.facebook.com","https://www.google.com","https://www.amazon.in"]\n\ndef checkValidURL(url):\n    url_reg_ex = r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\\?([^#]*))?(#(.*))?"\n    data = re.search(url_reg_ex,url)\n    if data is not None:\n        return True\n    return False\n\ndef parseDomain(url):\n    domain = url.split("//")[1].split("www")[1].split(".")[1]\n    print(domain)\n\n\nif __name__ == "__main__":\n    for url in urls:\n        url_status = checkValidURL(url)\n        if url_status:\n            parseDomain(url)\n\n\n    \n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Modifica el código para cambiar el comportamiento.\n#    (Pista: Intenta cambiar los valores de las variables o la lógica)\n# 3. Vuelve a ejecutar para ver tus cambios.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Consulta el repositorio oficial para más contexto.",
            type="interactive"
        ),
        Lesson(
            id=50,
            title="Introducción a Clases y Objetos",
            content='Estudia el siguiente código: Introducción a Clases y Objetos',
            example_code='"""\nLas clases son "plantillas" para crear objetos.\nLos objetos agrupan datos (atributos) y comportamientos (métodos).\n"""\n\nclass Laptop:\n    # El método __init__ es el constructor. Se ejecuta al crear un objeto.\n    def __init__(self, marca, modelo, ram):\n        self.marca = marca\n        self.modelo = modelo\n        self.ram = ram\n        self.encendida = False\n\n    def encender(self):\n        self.encendida = True\n        print(f"{self.marca} {self.modelo} se está encendiendo...")\n\n    def apagar(self):\n        self.encendida = False\n        print(f"{self.marca} {self.modelo} se está apagando...")\n\n    def info(self):\n        estado = "Encendida" if self.encendida else "Apagada"\n        print(f"Laptop: {self.marca} {self.modelo} | RAM: {self.ram} | Estado: {estado}")\n\n# Crear objetos (instancias) de la clase Laptop\nmi_laptop = Laptop("Dell", "XPS 13", "16GB")\ntu_laptop = Laptop("Apple", "MacBook Pro", "32GB")\n\n# Usar los objetos\nmi_laptop.info()\ntu_laptop.info()\n\nmi_laptop.encender()\nmi_laptop.info()\n\n# --- EJERCICIO INTERACTIVO ---\n# 1. Ejecuta el código tal como está para ver el resultado.\n# 2. Crea una nueva instancia de Laptop con tus datos.\n# 3. Llama a los métodos encender() y apagar() de tu nueva laptop.\n',
            exercise_prompt="Ejecuta el código y analiza su funcionamiento.",
            validator=lambda code: (True, "¡Ejercicio completado!"),
            hint="Las clases permiten modelar objetos del mundo real.",
            type="interactive"
        ),
    ]
)
