import json
import re
import os

# Paths
BASE_DIR = "/home/devilspy/.gemini/antigravity/scratch/python_tutor"
EXERCISES_JSON = os.path.join(BASE_DIR, "public/static/exercises_v2.json")
OUTPUT_JSON = os.path.join(BASE_DIR, "public/static/js/knowledge_base_lite.json")
TEXT_FILES = [
    os.path.join(BASE_DIR, "part1.txt"),
    os.path.join(BASE_DIR, "part2.txt"),
    os.path.join(BASE_DIR, "part3.txt")
]

def load_exercises_db():
    with open(EXERCISES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a map of Title -> ID
    title_map = {}
    for module in data:
        for lesson in module.get('lessons', []):
            # Normalize title for matching
            norm_title = normalize_text(lesson['title'])
            title_map[norm_title] = lesson['id']
    return title_map

def normalize_text(text):
    return text.lower().strip().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def parse_text_files():
    lessons_data = {}
    
    current_lesson = None
    current_section = None
    buffer = []

    regex_lesson = re.compile(r"^--- Lección: (.+) ---")
    regex_section = re.compile(r"^### (.+)")

    for file_path in TEXT_FILES:
        print(f"Processing {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            
            # New Lesson
            match_lesson = regex_lesson.match(line)
            if match_lesson:
                # Save previous section of previous lesson
                if current_lesson and current_section:
                    lessons_data[current_lesson][current_section] = "\n".join(buffer).strip()
                
                # Start new lesson
                title = match_lesson.group(1).strip()
                current_lesson = normalize_text(title)
                lessons_data[current_lesson] = {"title_raw": title}
                current_section = None
                buffer = []
                continue

            # New Section
            match_section = regex_section.match(line)
            if match_section:
                # Save previous section
                if current_lesson and current_section:
                    lessons_data[current_lesson][current_section] = "\n".join(buffer).strip()
                
                # Start new section
                raw_section = match_section.group(1).strip()
                # Map section names to keys
                if "Objetivo" in raw_section: current_section = "summary"
                elif "Aprendizaje" in raw_section: current_section = "concepts"
                elif "Instrucciones" in raw_section: current_section = "instructions"
                elif "Explicación" in raw_section: current_section = "explanation"
                else: current_section = "other"
                
                buffer = []
                continue

            # Content
            if current_lesson and current_section:
                if line: # Skip empty lines at start, but keep paragraphs
                    buffer.append(line)
                elif buffer: # Keep empty lines if we already have content (paragraph break)
                    buffer.append(line)

        # Save last section of last lesson
        if current_lesson and current_section:
            lessons_data[current_lesson][current_section] = "\n".join(buffer).strip()

    return lessons_data

def generate_kb():
    print("Loading Exercises DB...")
    id_map = load_exercises_db()
    
    print("Parsing Text Files...")
    parsed_lessons = parse_text_files()
    
    kb_data = {}
    matched_count = 0
    
    print(f"Found {len(parsed_lessons)} lessons in text files.")
    
    for norm_title, data in parsed_lessons.items():
        # Try to find ID
        exercise_id = id_map.get(norm_title)
        
        # Try fuzzy match if exact fails
        if not exercise_id:
            for db_title, db_id in id_map.items():
                if norm_title in db_title or db_title in norm_title:
                    exercise_id = db_id
                    break
        
        if exercise_id:
            kb_data[exercise_id] = {
                "summary": data.get("summary", ""),
                "explanation": data.get("explanation", ""),
                "concepts": data.get("concepts", "").replace("- ", ""), # Clean up list format
                "line_by_line": data.get("instructions", ""), # Use instructions as step-by-step for now
                "errors": {} # We don't have specific error data in text files, keep empty
            }
            matched_count += 1
        else:
            print(f"Warning: Could not match lesson '{data['title_raw']}' to an ID.")

    print(f"Matched {matched_count} exercises.")
    
    # Merge with existing manual data (don't overwrite good manual data if exists)
    # Actually, let's overwrite for consistency, but maybe keep manual errors if we had them?
    # For now, just write the generated data.
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=4, ensure_ascii=False)
    
    print(f"Knowledge Base saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_kb()
