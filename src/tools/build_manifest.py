import os
import json
import sys
import importlib

# Add current directory to path
sys.path.append(os.getcwd())

output_file = "public/static/exercises.json"
modules_data = []

# List files in exercises directory
exercises_dir = "data/exercises"
files = sorted([f for f in os.listdir(exercises_dir) if f.startswith("module_") and f.endswith(".py")])

print(f"Found {len(files)} module files.")

for filename in files:
    module_name = filename[:-3]
    full_module_name = f"data.exercises.{module_name}"
    
    try:
        print(f"Importing {full_module_name}...")
        module = importlib.import_module(full_module_name)
        
        if hasattr(module, "MODULE"):
            m = module.MODULE
            lessons = []
            for l in m.lessons:
                lessons.append({
                    "id": l.id,
                    "title": l.title,
                    "content": l.content,
                    "example_code": l.example_code,
                    "exercise_prompt": l.exercise_prompt,
                    "hint": l.hint,
                    "type": l.type
                })
            
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "lessons": lessons
            })
            print(f"Processed {module_name}")
    except Exception as e:
        print(f"Error processing {module_name}: {e}")

with open(output_file, "w") as f:
    json.dump(modules_data, f, indent=2)

print(f"Manifest generated at {output_file}")
