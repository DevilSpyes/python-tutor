
import json
import re
import os
from collections import Counter

# Path to exercises file
EXERCISES_PATH = '/home/devilspy/.gemini/antigravity/scratch/python_tutor/public/static/exercises_v2.json'

# Common Python keywords to look for explicitly
KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 
    'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    'int', 'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple', 'range', 'len',
    'print', 'input', 'type'
}

def extract_commands():
    if not os.path.exists(EXERCISES_PATH):
        print(f"Error: File not found at {EXERCISES_PATH}")
        return

    with open(EXERCISES_PATH, 'r', encoding='utf-8') as f:
        modules = json.load(f)

    command_counts = Counter()
    
    # Regex for function calls: word followed by (
    func_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\(')
    
    # Regex for keywords: exact word match
    keyword_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b')

    for module in modules:
        for lesson in module.get('lessons', []):
            text_content = (lesson.get('content', '') + ' ' + lesson.get('example_code', '')).lower()
            
            # Find function calls
            funcs = func_pattern.findall(text_content)
            for f in funcs:
                if len(f) > 2: # Ignore short noise
                    command_counts[f] += 1
            
            # Find keywords
            words = keyword_pattern.findall(text_content)
            for w in words:
                if w in KEYWORDS:
                    command_counts[w] += 1

    # Filter and sort
    # We keep anything that appears at least once if it's a keyword, 
    # or at least twice if it's a function call (to avoid variable names)
    
    final_commands = set()
    
    for cmd, count in command_counts.items():
        if cmd in KEYWORDS:
            final_commands.add(cmd)
        elif count >= 2: # Heuristic: if used multiple times, likely a command/method
            final_commands.add(cmd)

    # Manual cleanup of common non-commands
    ignore_list = {'exercise', 'solution', 'result', 'value', 'item', 'data', 'text', 'line', 'number', 'user', 'name', 'main'}
    final_commands = {c for c in final_commands if c not in ignore_list}

    print("Found commands:")
    for cmd in sorted(final_commands):
        print(cmd)

if __name__ == "__main__":
    extract_commands()
