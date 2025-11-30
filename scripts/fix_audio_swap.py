import os
import re
import asyncio
import edge_tts

# Save directly to public/audio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "../public/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def main():
    with open("exercise_scripts.txt", "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("Pasemos al siguiente ejercicio.")
    
    nmap_block = None
    cert_block = None
    
    for block in blocks:
        if "Nmap-like" in block:
            nmap_block = block
        if "Obtener Certificado" in block:
            cert_block = block
            
    if not nmap_block:
        print("Error: Could not find Nmap block.")
        return
    if not cert_block:
        print("Error: Could not find Certificado block.")
        return

    # Generate Nmap Audio (File 117)
    filename_nmap = "117_module_06_proyecto_final_escaner_de_red_avanzado_nmap_like.mp3"
    filepath_nmap = os.path.join(OUTPUT_DIR, filename_nmap)
    text_nmap = nmap_block.strip().replace("Python", "Páiton")
    
    print(f"Generating {filename_nmap}...")
    try:
        communicate = edge_tts.Communicate(text_nmap, "es-ES-AlvaroNeural")
        await communicate.save(filepath_nmap)
        print(f"Successfully generated {filepath_nmap}")
    except Exception as e:
        print(f"Error generating {filename_nmap}: {e}")

    # Generate Certificado Audio (File 119)
    filename_cert = "119_module_07_obtener_certificado.mp3"
    filepath_cert = os.path.join(OUTPUT_DIR, filename_cert)
    text_cert = cert_block.strip().replace("Python", "Páiton")
    
    print(f"Generating {filename_cert}...")
    try:
        communicate = edge_tts.Communicate(text_cert, "es-ES-AlvaroNeural")
        await communicate.save(filepath_cert)
        print(f"Successfully generated {filepath_cert}")
    except Exception as e:
        print(f"Error generating {filename_cert}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
