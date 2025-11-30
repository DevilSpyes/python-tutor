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
    
    # We only want the first block (Module 00)
    block = blocks[0]
    
    current_module = "00"
    file_counter = 1 

    text = block.strip()
    if not text or text == ".":
        print("Error: First block is empty or invalid.")
        return

    # Logic from generate_all_audios.py
    module_match = re.search(r"Módulo (\d+)", text)
    if module_match:
        current_module = module_match.group(1)
        
    lesson_match = re.search(r"Lección: (.*?)\.", text)
    if lesson_match:
        lesson_title = lesson_match.group(1)
    elif "Módulo 00" in text:
        lesson_title = "Bienvenida"
    else:
        lesson_title = "Intro"

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
