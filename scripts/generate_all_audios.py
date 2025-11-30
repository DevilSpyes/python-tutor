import os
import re
import asyncio
import edge_tts

OUTPUT_DIR = "audio_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def main():
    with open("exercise_scripts.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Split by the separator
    # The separator "Pasemos al siguiente ejercicio." is used to delimit blocks.
    blocks = content.split("Pasemos al siguiente ejercicio.")
    
    current_module = "00"
    file_counter = 1 # Start at 1

    print(f"Found {len(blocks)} blocks to process.")

    for block in blocks:
        text = block.strip()
        # Skip empty blocks or blocks with just dots
        if not text or text == ".":
            continue
            
        # Update Module context if present
        # Pattern: Módulo 01: Introducción
        module_match = re.search(r"Módulo (\d+)", text)
        if module_match:
            current_module = module_match.group(1)
            
        # Find Lesson Title
        # Pattern: Lección: Hola Mundo.
        lesson_match = re.search(r"Lección: (.*?)\.", text)
        if lesson_match:
            lesson_title = lesson_match.group(1)
        elif "Módulo 00" in text:
            lesson_title = "Bienvenida"
        else:
            # If it's just a module header block without a specific lesson (e.g. intro text), name it intro
            lesson_title = "Intro"

        # Sanitize filename
        # Remove accents
        normalization_map = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N'
        }
        for k, v in normalization_map.items():
            lesson_title = lesson_title.replace(k, v)
            
        safe_title = re.sub(r"[^a-zA-Z0-9]", "_", lesson_title).lower()
        safe_title = re.sub(r"_+", "_", safe_title).strip("_")
        
        filename = f"{file_counter:03d}_module_{current_module}_{safe_title}.mp3"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Fix Pronunciation
        text_to_speak = text.replace("Python", "Páiton")
        
        # Generate
        print(f"[{file_counter}/{len(blocks)}] Generating {filename}...")
        try:
            communicate = edge_tts.Communicate(text_to_speak, "es-ES-AlvaroNeural")
            await communicate.save(filepath)
        except Exception as e:
            print(f"Error generating {filename}: {e}")
        
        file_counter += 1

    print(f"\nGeneration complete. Files saved to {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    asyncio.run(main())
