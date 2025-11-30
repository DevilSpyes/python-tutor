import os
import json
import asyncio
import edge_tts

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "../public/audio")
MANIFEST_PATH = os.path.join(BASE_DIR, "../public/audio/manifest.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def main():
    # 1. Define the text explicitly to avoid any parsing errors
    text_nmap = """
Lección: Proyecto Final: Escáner de Red Avanzado (Nmap-like).

El objetivo de este ejercicio es:
Desarrollar una herramienta de escaneo de red robusta y continua, similar a Nmap.

En esta lección aprenderemos:
Escaneo de múltiples puertos en bucle.
Manejo de timeouts y errores de conexión.
Creación de menús interactivos en consola.
Validación de rangos de direcciones IP.

Para realizar el ejercicio, sigue estas instrucciones:
Paso 1: Ejecuta el script y selecciona la opción de escaneo rápido.
Paso 2: Introduce la IP de tu máquina local (localhost) o una de tu red.
Paso 3: Observa cómo la herramienta descubre los puertos abiertos en tiempo real.

Permíteme explicarte más detalles.
Este es el desafío final de ciberseguridad. Vamos a combinar todo lo aprendido: sockets, bucles, control de flujo y manejo de errores.

A diferencia del escáner simple anterior, esta herramienta está diseñada para ser persistente y robusta. Implementaremos un menú principal que permita realizar múltiples escaneos sin cerrar el programa, y mejoraremos la detección de puertos para evitar falsos negativos. Es una herramienta que podrías usar en una auditoría real básica.
""".strip().replace("Python", "Páiton")

    text_cert = """
Lección: Obtener Certificado.

El objetivo de este ejercicio es:
Generar un diploma personalizado en PDF como recompensa final.

En esta lección aprenderemos:
Uso avanzado de fpdf2.
Posicionamiento absoluto y alineación.
Inserción de fechas dinámicas.

Para realizar el ejercicio, sigue estas instrucciones:
Paso 1: IMPORTANTE: Edita el código y pon TU NOMBRE en la variable nombre_estudiante.
Paso 2: Ejecuta el script.
Paso 3: ¡Disfruta de tu certificado de finalización! Te lo has ganado.

Permíteme explicarte más detalles.
¡Felicidades! Han llegado al final del curso.

Como último ejercicio, usarán todo lo aprendido para generar su propio certificado de finalización. Este script crea un PDF con diseño profesional, inserta su nombre y la fecha actual. Es un recuerdo tangible de su esfuerzo y aprendizaje.
""".strip().replace("Python", "Páiton")

    # 2. Generate Files with NEW names
    file_nmap = "fixed_nmap_project.mp3"
    file_cert = "fixed_certificate.mp3"
    
    path_nmap = os.path.join(OUTPUT_DIR, file_nmap)
    path_cert = os.path.join(OUTPUT_DIR, file_cert)

    print(f"Generating {file_nmap}...")
    try:
        communicate = edge_tts.Communicate(text_nmap, "es-ES-AlvaroNeural")
        await communicate.save(path_nmap)
        print(f"Saved to {path_nmap}")
    except Exception as e:
        print(f"Error generating Nmap audio: {e}")

    print(f"Generating {file_cert}...")
    try:
        communicate = edge_tts.Communicate(text_cert, "es-ES-AlvaroNeural")
        await communicate.save(path_cert)
        print(f"Saved to {path_cert}")
    except Exception as e:
        print(f"Error generating Cert audio: {e}")

    # 3. Update Manifest
    print("Updating manifest.json...")
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    # Update IDs (115 for Nmap, 116 for Certificado)
    # NOTE: Check if IDs are correct in your system. 
    # Based on previous checks: 
    # 115 -> Nmap
    # 116 -> Certificado
    
    manifest["115"] = file_nmap
    manifest["116"] = file_cert

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print("Manifest updated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
