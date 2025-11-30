import os
import re
import asyncio
import edge_tts

# Save directly to public/audio
OUTPUT_DIR = "../public/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def main():
    with open("exercise_scripts.txt", "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("Pasemos al siguiente ejercicio.")
    
    target_block = None
    for block in blocks:
        if "Lección: Conversión de Tipos" in block:
            target_block = block
            break
            
    if not target_block:
        print("Error: Could not find the lesson block.")
        return

    text = target_block.strip()
    
    # Hardcoded filename to match existing one
    filename = "005_module_01_conversion_de_tipos_casting.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Fix Pronunciation
    text_to_speak = text.replace("Python", "Páiton")
    
    print(f"Generating {filename}...")
    try:
        communicate = edge_tts.Communicate(text_to_speak, "es-ES-AlvaroNeural")
        await communicate.save(filepath)
        print(f"Successfully generated {filepath}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
