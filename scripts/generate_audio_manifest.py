import os
import json
import glob
import sys

# Add project root to path to import data.exercises
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.exercises import Module, Lesson

def main():
    # 1. Get all lessons in order
    base_dir = os.path.join(os.path.dirname(__file__), '../data/exercises')
    module_files = sorted(glob.glob(os.path.join(base_dir, 'module_*.py')))
    
    all_lessons = []
    
    for file_path in module_files:
        # We need to import the module to access the object
        # Using a simple exec to avoid complex import logic
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Create a dummy environment
        local_env = {'Module': Module, 'Lesson': Lesson}
        try:
            exec(source, {}, local_env)
            module_obj = local_env.get('MODULE')
            if module_obj:
                # Sort lessons by ID just in case, or trust the list order?
                # Trusting list order is safer if IDs are not perfectly sequential globally (though they seem to be)
                # But wait, IDs are what the frontend uses.
                # Let's assume the order in the file matches the order in exercise_scripts.txt
                all_lessons.extend(module_obj.lessons)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    print(f"Found {len(all_lessons)} lessons.")

    # 2. Get all audio files in order
    audio_dir = os.path.join(os.path.dirname(__file__), '../public/audio')
    audio_files = sorted(glob.glob(os.path.join(audio_dir, '*.mp3')))
    
    print(f"Found {len(audio_files)} audio files.")
    
    if len(all_lessons) != len(audio_files):
        print("WARNING: Mismatch in count! Mapping might be incorrect.")
        # We will proceed but warn
    
    # 3. Create mapping
    manifest = {}
    
    # Zip them. We assume the sort order of filenames (001, 003...) corresponds to the lesson order.
    for lesson, audio_path in zip(all_lessons, audio_files):
        filename = os.path.basename(audio_path)
        manifest[str(lesson.id)] = filename
        print(f"Mapped Lesson {lesson.id} ({lesson.title}) -> {filename}")

    # 4. Save manifest
    manifest_path = os.path.join(audio_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Manifest saved to {manifest_path}")

if __name__ == "__main__":
    main()
