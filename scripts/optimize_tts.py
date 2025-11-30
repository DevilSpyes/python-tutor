import re
import os

def optimize_for_tts(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    optimized_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            optimized_lines.append("")
            continue

        # General Cleanup (Apply to all lines first)
        line = line.replace("`", "")
        line = line.replace("**", "")
        line = line.replace("*", "")
        line = line.replace("#", "")

        # Header Replacements
        if line.startswith("===") and line.endswith("==="):
            # Remove Module headers from spoken text
            continue
        
        if line.startswith("--- Lección:") and line.endswith("---"):
            # Remove Lesson headers from spoken text but keep separation
            # Add separation phrase
            optimized_lines.append("\n\nPasemos al siguiente ejercicio.\n")
            continue

        # Section Headers -> Narrative Transitions
        if "Objetivo" in line and "🎯" in line:
             optimized_lines.append("El objetivo de este ejercicio es:")
             continue
        if "Objetivo del ejercicio:" in line: # Handle already optimized lines if re-running
             optimized_lines.append("El objetivo de este ejercicio es:")
             continue
             
        if "Aprendizaje" in line and "🧠" in line:
            optimized_lines.append("En esta lección aprenderemos:")
            continue
        if "Puntos clave de aprendizaje:" in line:
            optimized_lines.append("En esta lección aprenderemos:")
            continue

        if "Instrucciones" in line and "📝" in line:
            optimized_lines.append("Para realizar el ejercicio, sigue estas instrucciones:")
            continue
        if "Instrucciones paso a paso:" in line:
             optimized_lines.append("Para realizar el ejercicio, sigue estas instrucciones:")
             continue

        if "Explicación" in line and "👨‍🏫" in line:
            optimized_lines.append("Permíteme explicarte más detalles.")
            continue
        if "Explicación detallada:" in line:
            optimized_lines.append("Permíteme explicarte más detalles.")
            continue

        # List Cleaning
        if line.startswith("- "):
            # Bullet points: - Item -> Item.
            clean_line = line[2:].strip()
            optimized_lines.append(f"{clean_line}")
            continue
        
        # Numbered Lists: 1. Step -> Paso 1: Step
        match = re.match(r"^(\d+)\.\s+(.*)", line)
        if match:
            number = match.group(1)
            text = match.group(2)
            optimized_lines.append(f"Paso {number}: {text}")
            continue

        optimized_lines.append(line)

    # Join and save
    output_content = "\n".join(optimized_lines)
    
    # Post-processing to ensure no double empty lines
    output_content = re.sub(r'\n{3,}', '\n\n', output_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"Optimized content saved to {output_file}")

if __name__ == "__main__":
    input_path = "/home/devilspy/.gemini/antigravity/scratch/python_tutor/exercise_scripts.txt"
    # We will overwrite the file as per plan, but let's keep a backup just in case for now or write to same file
    # The plan said overwrite.
    optimize_for_tts(input_path, input_path)
