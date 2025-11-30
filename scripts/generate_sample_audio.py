import asyncio
import edge_tts
import re

async def generate_sample():
    # 1. Read the first exercise from the file
    with open("exercise_scripts.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract Module 00 content (up to the start of Module 01)
    # We'll just take the first lesson of Module 00 for the sample
    # Pattern: From "Módulo 00: Bienvenida y Guía." to "Pasemos al siguiente ejercicio."
    
    start_marker = "Módulo 00: Bienvenida y Guía."
    end_marker = "Pasemos al siguiente ejercicio."
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)
    
    if start_index == -1 or end_index == -1:
        print("Error: Could not find the first lesson.")
        return

    # Skip the header itself
    text_to_speak = content[start_index + len(start_marker):end_index].strip()
    
    # Fix pronunciation for "Python"
    text_to_speak = text_to_speak.replace("Python", "Páiton")
    
    # Do NOT prepend title as per user request
    # text_to_speak = "Módulo 00: Bienvenida y Guía.\n\n" + text_to_speak
    
    print(f"Generating audio for text:\n{'-'*20}\n{text_to_speak}\n{'-'*20}")
    
    # 2. Generate Audio
    voice = "es-ES-AlvaroNeural" # Similar to Enrique
    output_file = "sample_module_00.mp3"
    
    communicate = edge_tts.Communicate(text_to_speak, voice)
    await communicate.save(output_file)
    
    print(f"Audio saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_sample())
