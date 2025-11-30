import json
import re

raw_data = """
01–20: Conceptos iniciales – Hola Mundo, datos, variables
¿Qué hace el código print("Hola Mundo")? → Imprime texto en pantalla.
¿Para qué sirve print()? → Para mostrar información en la consola.
¿Qué es una variable? → Es un espacio que guarda un valor.
¿Qué es un tipo de dato? → La categoría del valor (str, int, etc.).
¿Qué significa string? → Texto.
¿Qué significa integer? → Número entero.
¿Qué es float? → Número con decimales.
¿Qué es boolean? → True/False.
¿Qué es input()? → Pide un dato al usuario.
¿Para qué sirve int()? → Convierte a número entero.
¿Para qué sirve str()? → Convierte a texto.
¿Qué hace type()? → Muestra el tipo de dato.
¿Qué significa “casting”? → Convertir tipos de datos.
¿Qué es un comentario? → Texto ignorado por Python.
¿Cómo se escribe un comentario? → Con #.
¿Qué es un error de sintaxis? → Código escrito incorrectamente.
¿Qué es un operador? → Símbolo que realiza operaciones.
¿Qué es concatenar? → Unir textos.
¿Por qué aparece error al sumar string + int? → Tipos incompatibles.
¿Cómo soluciono string + int? → Convertir ambos al mismo tipo.

21–40: Condicionales
¿Qué hace un if? → Ejecuta código si se cumple una condición.
¿Qué hace un else? → Ejecuta código si el if falla.
¿Qué hace elif? → Evalúa una condición adicional.
¿Qué es ==? → Comparación de igualdad.
¿Qué es !=? → Distinto.
¿Qué es >? → Mayor que.
¿Qué es < ? → Menor que.
¿Qué significa or? → Al menos una condición verdadera.
¿Qué significa and? → Todas deben ser verdaderas.
¿Qué significa not? → Niega un valor.
¿Qué es indentación? → Sangría obligatoria en Python.
¿Por qué falla mi if? → Generalmente por mala indentación.
¿Qué es una condición booleana? → Una expresión True/False.
¿Cómo comparo cadenas? → Con ==.
¿Qué pasa si no pongo los : ? → Error de sintaxis.
¿Puedo anidar if? → Sí.
¿Qué es una condición múltiple? → Varios if/elif/else.
¿Qué es un bloque de código? → Instrucciones dentro de una indentación.
¿Qué es una rama del programa? → Ruta según la condición.
¿Por qué siempre entra al else? → El if nunca se cumple.

41–60: Listas y métodos
¿Qué es una lista? → Colección ordenada de elementos.
¿Cómo se crea una lista? → Con corchetes [].
¿Qué hace append()? → Agrega un elemento.
¿Qué hace pop()? → Quita un elemento.
¿Qué hace remove()? → Elimina por valor.
¿Qué hace sort()? → Ordena.
¿Qué hace len()? → Devuelve la cantidad de elementos.
¿Cómo accedo al primer elemento? → lista[0].
¿Cómo accedo al último? → lista[-1].
¿Cómo reemplazo un elemento? → lista[i] = valor.
¿Qué es slicing? → Extraer partes de una lista.
¿Para qué sirve insert()? → Insertar en un índice específico.
¿Qué hace reverse()? → Invierte el orden.
¿Cómo verifico si algo está en la lista? → valor in lista.
¿Qué pasa si accedo a un índice inexistente? → Error IndexError.
¿Qué es una lista vacía? → [].
¿Qué tipo de dato puede tener una lista? → Cualquiera.
¿Qué es una lista mixta? → Varios tipos de datos.
¿Cómo duplico una lista? → lista.copy().
¿Qué es un bucle sobre una lista? → Recorrer elementos uno a uno.

61–90: Bucles While y For
¿Qué es un bucle? → Repite código.
¿Qué es un while? → Repite mientras la condición sea True.
¿Qué es un for? → Recorre elementos.
¿Qué es range()? → Genera secuencias de números.
¿Qué hace break? → Sale del bucle.
¿Qué hace continue? → Salta a la siguiente vuelta.
¿Por qué mi while nunca termina? → La condición nunca cambia.
¿Qué es un bucle infinito? → Un while que nunca acaba.
¿Qué hace for x in lista? → Itera valores.
¿Qué hace for i in range(n)? → Repite n veces.
¿Qué es una iteración? → Una vuelta del bucle.
¿Qué pasa si range es range(1,10)? → Va del 1 al 9.
¿Qué pasa si range es range(0,10,2)? → Números pares del 0 al 8.
¿Qué pasa si uso break? → Sale inmediatamente.
¿Qué pasa si uso continue? → Salta a la siguiente vuelta.
¿Cómo contar elementos? → Con un contador += 1.
¿Cómo sumar números en bucle? → Acumulador.
¿Qué es i en un for? → Variable temporal del bucle.
¿Qué es iterar? → Repetir sobre cada elemento.
¿Para qué sirve enumerate()? → Obtener índice y valor.
¿Qué es un for anidado? → Un for dentro de otro.
¿Qué significa range(len(lista))? → Iterar índices.
¿Qué es un contador? → Variable que incrementa.
¿Qué es un acumulador? → Variable que suma o guarda datos.
¿Qué es un patrón de bucle? → Estructuras típicas de iteración.
¿Cuándo usar while y no for? → Cuando no conoces cuántas repeticiones habrá.
¿Cuándo usar for y no while? → Cuando iteras una secuencia.
¿Por qué mi for no entra nunca? → La lista está vacía.
¿Qué es un rango vacío? → range(0,0).
¿Puedo usar break en un for? → Sí.

91–130: Funciones
¿Qué es una función? → Código reutilizable.
¿Cómo crear una función? → Con def.
¿Qué es return? → Devuelve un resultado.
¿Qué es un parámetro? → Valor que entra.
¿Qué es un argumento? → El valor pasado al llamar.
¿Para qué sirve una función? → Para organizar código.
¿Qué pasa si no pongo return? → Devuelve None.
¿Qué es una función vacía? → Que no devuelve nada.
¿Qué es un valor por defecto? → Parámetro predefinido.
¿Qué es *args? → Múltiples argumentos.
¿Qué es **kwargs? → Argumentos nombrados.
¿Qué es scope? → Alcance de variables.
¿Qué es variable local? → Solo dentro de la función.
¿Qué es variable global? → Fuera de la función.
¿Por qué mi return no funciona? → Código después del return no se ejecuta.
¿Puedo retornar varios valores? → Sí, en tuplas.
¿Qué es documentar una función? → Explicar qué hace.
¿Qué es docstring? → Texto explicativo dentro de la función.
¿Qué es modularidad? → Dividir el código en funciones.
¿Qué es reutilización? → Usar funciones repetidamente.
¿Puedo llamar una función desde otra? → Sí.
¿Por qué no se ejecuta mi función? → Falta llamarla.
¿Qué significa def suma(a, b)? → Crear función suma.
¿Qué es una función pura? → Sin efectos secundarios.
¿Qué es un side effect? → Cambios fuera de la función.

116. ¿Qué es una variable en Python?
Una variable es un nombre que almacena un valor en memoria para poder reutilizarlo o modificarlo.

117. ¿Cómo declaro una variable?
Solo asignas un valor con =:
x = 10

118. ¿Qué tipos de datos existen en Python?
Enteros, flotantes, cadenas, booleanos, listas, tuplas, diccionarios y conjuntos.

119. ¿Qué es un entero (int)?
Un número sin decimales, como 5 o -12.

120. ¿Qué es un flotante (float)?
Un número con decimales, como 5.3 o -0.75.

121. ¿Qué es un string?
Una cadena de texto entre comillas: "hola".

122. ¿Qué es un booleano?
Un valor lógico: True o False.

123. ¿Cómo convierto un string a número?
Usando int() o float().

124. ¿Cómo convierto un número a string?
Usando str().

125. ¿Qué pasa si convierto texto no numérico a número?
Ocurre un error ValueError.

126. ¿Cómo pido datos al usuario?
Usando input().

127. ¿Qué devuelve input()?
Siempre un string.

128. ¿Cómo hago un comentario de una línea?
Usando #.

129. ¿Cómo hago un comentario multilínea?
Usando triple comillas:
\"\"\"
texto
\"\"\"

130. ¿Qué es una condición if?
Una estructura que ejecuta código solo si se cumple una expresión.

131. ¿Cómo escribo un if básico?
if x > 5:
    print("Mayor")

132. ¿Qué es un else?
La parte que se ejecuta cuando el if no se cumple.

133. ¿Qué es un elif?
Una condición extra entre if y else.

134. ¿Qué es un operador lógico?
Palabras como and, or, not.

135. ¿Qué hace and?
Requiere que ambas condiciones sean verdaderas.

136. ¿Qué hace or?
Requiere que al menos una condición sea verdadera.

137. ¿Qué hace not?
Invierte un valor booleano.

138. ¿Qué es una lista?
Una colección ordenada y modificable de valores:
[1, 2, 3]

139. ¿Cómo accedo a un elemento de una lista?
Con su índice:
lista[0]

140. ¿Cómo cambio un dato de una lista?
lista[1] = 50

141. ¿Cómo agrego un elemento a una lista?
lista.append(10)

142. ¿Cómo elimino un elemento de una lista?
lista.remove(10)

143. ¿Cómo elimino por índice?
del lista[0]

144. ¿Qué es un bucle while?
Un ciclo que se ejecuta mientras la condición sea verdadera.

145. ¿Cómo escribo un while?
while x < 5:
    x += 1

146. ¿Qué es un bucle for?
Un ciclo que recorre elementos de una colección.

147. ¿Cómo recorro una lista con for?
for n in lista:
    print(n)

148. ¿Qué hace range()?
Genera secuencias de números como 0,1,2,....

149. ¿Cómo uso range()?
for i in range(5):
    print(i)

150. ¿Qué es una función?
Bloque de código reutilizable.

151. ¿Cómo creo una función?
def saludar():
    print("Hola")

152. ¿Cómo regreso un valor desde una función?
Con return.

153. ¿Qué es un diccionario?
Estructura de pares clave‑valor:
{"nombre": "Ana", "edad": 20}

154. ¿Cómo accedo a una clave del diccionario?
dic["nombre"]

155. ¿Cómo agrego una clave nueva?
dic["ciudad"] = "Madrid"

156. ¿Cómo verifico si una clave existe?
"nombre" in dic

157. ¿Qué es una tupla?
Secuencia inmutable de valores:
(1, 2, 3)

158. ¿Qué es un set?
Conjunto sin orden y sin duplicados.

159. ¿Cómo hago un set?
{1, 2, 3}

160. ¿Qué es un error try/except?
Bloque que captura errores para evitar que el programa falle.

161. ¿Cómo uso try/except?
try:
    x = int("hola")
except:
    print("Error")

162. ¿Qué es break?
Detiene un bucle.

163. ¿Qué es continue?
Salta a la siguiente iteración del bucle.

164. ¿Qué es un operador de comparación?
Símbolos como ==, !=, <, >.

165. ¿Qué es un operador lógico?
and, or, not (ya explicados).

166. ¿Cómo formateo texto con f‑strings?
name = "Ana"
print(f"Hola {name}")

167. ¿Qué son métodos de strings?
Funciones internas como .upper(), .lower(), .strip().

168. ¿Qué hace .upper()?
Convierte el texto a mayúsculas.

169. ¿Qué hace .lower()?
Convierte a minúsculas.

170. ¿Qué hace .strip()?
Elimina espacios al inicio y final.

171. ¿Qué hace .split()?
Divide un string en una lista.

172. ¿Qué hace .join()?
Une una lista en un string.

173. ¿Qué es un loop anidado?
Un bucle dentro de otro.

174. ¿Qué es un return múltiple?
Retornar más de un valor en una tupla.

175. ¿Cómo documento una función?
Con docstrings:
def f():
    \"\"\"Explica qué hace la función.\"\"\"

176. ¿Qué es un diccionario en Python?
Un diccionario es una estructura que almacena pares clave‑valor, permitiendo acceder a la información mediante claves en lugar de índices.

177. ¿Cómo accedo al valor de una clave en un diccionario?
Usando diccionario["clave"].

178. ¿Cómo añado un nuevo par clave‑valor a un diccionario?
Asignando: diccionario["nueva_clave"] = valor.

179. ¿Cómo elimino una clave de un diccionario?
Con del diccionario["clave"].

180. ¿Qué hace el método .get() en un diccionario?
Devuelve el valor de una clave sin lanzar error si la clave no existe.

181. ¿Para qué sirve el método .keys()?
Devuelve todas las claves del diccionario.

182. ¿Para qué sirve el método .values()?
Devuelve todos los valores del diccionario.

183. ¿Para qué sirve .items()?
Devuelve una lista de tuplas con clave y valor.

184. ¿Qué es una tupla en Python?
Una colección ordenada e inmutable.

185. ¿Cuándo usar una tupla en lugar de una lista?
Cuando los datos no deben cambiar.

186. ¿Cómo se crea una tupla?
Con paréntesis: tupla = (1, 2, 3).

187. ¿Cómo accedo a un elemento de una tupla?
Por índice: tupla[0].

188. ¿Qué es un set en Python?
Una colección desordenada de elementos únicos.

189. ¿Para qué sirve un set?
Para eliminar duplicados o hacer operaciones de conjuntos.

190. ¿Cómo se crea un set?
Con llaves: set1 = {1, 2, 3}.

191. ¿Cómo agrego un elemento a un set?
Con .add().

192. ¿Cómo elimino un elemento de un set?
Con .remove() o .discard().

193. ¿Qué es una función en Python?
Un bloque reutilizable de código que realiza una tarea.

194. ¿Cómo se define una función?
Con def nombre():.

195. ¿Qué es un parámetro?
Un valor que la función recibe para trabajar.

196. ¿Qué es un argumento?
El valor real que se pasa a la función.

197. ¿Qué hace return?
Devuelve un valor a quien llama la función.

198. ¿Qué es un valor por defecto en funciones?
Un parámetro que ya tiene asignado un valor inicial.

199. ¿Qué son las funciones lambda?
Funciones pequeñas y anónimas.

200. ¿Cómo se define una lambda?
lambda x: x * 2.

201. ¿Para qué sirve map()?
Aplica una función a cada elemento de un iterable.

202. ¿Para qué sirve filter()?
Filtra elementos según una condición.

203. ¿Qué hace sum()?
Suma todos los elementos numéricos de un iterable.

204. ¿Qué hace max()?
Obtiene el valor máximo.

205. ¿Qué hace min()?
Obtiene el mínimo.

206. ¿Qué hace len()?
Devuelve el número de elementos.

207. ¿Qué es una expresión regular?
Una secuencia de símbolos que describe patrones de texto.

208. ¿Para qué sirve re.search()?
Busca un patrón en un texto.

209. ¿Qué hace re.match()?
Verifica si el patrón coincide desde el inicio del texto.

210. ¿Qué hace re.findall()?
Devuelve todas las coincidencias encontradas.

211. ¿Qué hace re.sub()?
Reemplaza partes del texto que coinciden con el patrón.

212. ¿Qué es una clase?
Un molde para crear objetos.

213. ¿Qué es un objeto?
Una instancia de una clase.

214. ¿Qué es un método?
Una función dentro de una clase.

215. ¿Qué es __init__?
El constructor que se ejecuta al crear un objeto.

216. ¿Qué es self?
La referencia al propio objeto.

217. ¿Qué es la herencia en clases?
Una clase puede heredar atributos y métodos de otra.

218. ¿Cómo se define una clase hija?
class Hija(Padre):.

219. ¿Qué es la encapsulación?
Restringir acceso a datos internos.

220. ¿Qué es la sobreescritura de métodos?
Modificar un método heredado.

221. ¿Qué es un módulo en Python?
Un archivo .py con código reutilizable.

222. ¿Qué es una librería?
Un conjunto de módulos.

223. ¿Qué hace import?
Importa un módulo.

224. ¿Qué hace from x import y?
Importa solo una parte específica del módulo.

225. ¿Qué es un paquete en Python?
Una carpeta con módulos y un archivo __init__.py.

226. Pregunta: ¿Qué hace list.reverse()?
Respuesta: Invierte el orden de los elementos de la lista in place, sin crear una nueva.

227. Pregunta: ¿Qué diferencia hay entre reverse() y reversed()?
Respuesta: reverse() modifica la lista original; reversed() devuelve un iterador sin modificarla.

228. Pregunta: ¿Qué es un salto de línea?
Respuesta: Es el carácter especial \\n que indica que el texto continúa en la siguiente línea.

229. Pregunta: ¿Cómo quito espacios al inicio y final de un string?
Respuesta: Usando texto.strip().

230. Pregunta: ¿Qué hace texto.startswith("Hola")?
Respuesta: Devuelve True si el string comienza con “Hola”.

231. Pregunta: ¿Qué hace texto.endswith(".py")?
Respuesta: Devuelve True si el string termina en “.py”.

232. Pregunta: ¿Para qué sirve join en Python?
Respuesta: Para unir elementos de una lista en un solo string.

233. Pregunta: ¿Cómo convierto una lista en un string separado por comas?
Respuesta: ",".join(lista).

234. Pregunta: ¿Qué hace split()?
Respuesta: Divide un string en partes y devuelve una lista.

235. Pregunta: ¿Qué es un índice negativo?
Respuesta: Un índice que cuenta desde el final de la lista o string.

236. Pregunta: ¿Qué hace my_list[-1]?
Respuesta: Obtiene el último elemento de la lista.

237. Pregunta: ¿Qué es una función con parámetros opcionales?
Respuesta: Una función donde algunos parámetros tienen valores por defecto.

238. Pregunta: ¿Qué hace este código?
def saludo(nombre="Alumno"):
    print("Hola", nombre)
Respuesta: Si no pasas un nombre, usa “Alumno” por defecto.

239. Pregunta: ¿Qué es una función que retorna múltiples valores?
Respuesta: Es una función que devuelve varios valores como una tupla.

240. Pregunta: ¿Cómo retorno múltiples valores?
Respuesta: return a, b, c.

241. Pregunta: ¿Qué hace enumerate()?
Respuesta: Añade un contador al iterar una lista o colección.

242. Pregunta: ¿Qué hace este código?
for i, v in enumerate(lista):
    print(i, v)
Respuesta: Imprime el índice y el valor de cada elemento.

243. Pregunta: ¿Qué hace zip()?
Respuesta: Combina elementos de varias listas en tuplas.

244. Pregunta: ¿Qué hace este código?
list(zip([1,2], ["a","b"]))
Respuesta: Devuelve [(1, "a"), (2, "b")].

245. Pregunta: ¿Qué significa “inyección SQL” en el módulo de seguridad?
Respuesta: Manipular consultas SQL mediante entrada maliciosa.

246. Pregunta: ¿Qué es un hash de contraseña?
Respuesta: Una representación irreversible de una contraseña.

247. Pregunta: ¿Por qué no debo guardar contraseñas en texto plano?
Respuesta: Porque cualquiera que acceda al archivo las vería directamente.

248. Pregunta: ¿Qué hace un escáner de puertos?
Respuesta: Revisa qué puertos están abiertos en una máquina.

249. Pregunta: ¿Qué es una tupla en Python?
Respuesta: Una colección ordenada e inmutable.

250. Pregunta: ¿Cuándo usar una tupla en lugar de una lista?
Respuesta: Cuando los valores no deben cambiar.
"""

qa_list = []

# Pattern 1: Arrow format "Question? → Answer."
# Pattern 2: Numbered format "123. Question?\nAnswer"
# Pattern 3: "Pregunta: ...\nRespuesta: ..."

lines = raw_data.split('\n')
current_q = None
current_a = []

for line in lines:
    line = line.strip()
    if not line:
        continue
        
    # Pattern 1: Arrow
    if '→' in line:
        parts = line.split('→')
        q = parts[0].strip()
        a = parts[1].strip()
        # Clean leading numbers/bullets
        q = re.sub(r'^\d+[\.\–\-\)]\s*', '', q)
        qa_list.append({"q": q, "a": a})
        continue

    # Pattern 3: Pregunta/Respuesta
    if line.startswith("Pregunta:"):
        if current_q and current_a:
            qa_list.append({"q": current_q, "a": "\n".join(current_a)})
            current_a = []
        current_q = line.replace("Pregunta:", "").strip()
        continue
    if line.startswith("Respuesta:"):
        # Start capturing answer
        current_a = [line.replace("Respuesta:", "").strip()]
        continue
        
    # Pattern 2: Numbered Question
    # Check if line starts with number and dot
    if re.match(r'^\d+\.', line):
        if current_q and current_a:
            qa_list.append({"q": current_q, "a": "\n".join(current_a)})
            current_a = []
        current_q = re.sub(r'^\d+\.\s*', '', line)
        continue
        
    # Continuation of answer or question?
    # If we have a current_q but no current_a started (and not Pattern 3), then this line is likely the answer (Pattern 2 style)
    if current_q and not current_a and not line.startswith("Respuesta:"):
         current_a.append(line)
    elif current_q and current_a:
         current_a.append(line)

# Flush last
if current_q and current_a:
    qa_list.append({"q": current_q, "a": "\n".join(current_a)})

print(json.dumps(qa_list, indent=4, ensure_ascii=False))
