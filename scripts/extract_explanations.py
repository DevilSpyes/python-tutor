import ast
import os
import tokenize
from io import BytesIO
import glob

def extract_text_from_code(code_str):
    text_parts = []
    try:
        tokens = tokenize.tokenize(BytesIO(code_str.encode('utf-8')).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment = token.string.strip()
                # Remove the leading #
                if comment.startswith('#'):
                    comment = comment[1:].strip()
                
                # Skip shebangs and encoding declarations
                if comment.startswith('!') or comment.startswith('coding:'):
                    continue
                
                # Skip separator lines like "---" or "==="
                if set(comment) <= {'-', '=', ' '}:
                    continue

                if comment:
                    text_parts.append(comment)
            
            elif token.type == tokenize.STRING:
                s = token.string
                # Check for triple quotes indicating docstrings/multiline comments
                if s.startswith('"""') or s.startswith("'''"):
                    # Remove quotes
                    content = s[3:-3]
                    # Clean up lines
                    lines = [line.strip() for line in content.splitlines()]
                    clean_content = '\n'.join(line for line in lines if line)
                    if clean_content:
                        text_parts.append(clean_content)
    except tokenize.TokenError:
        pass
    
    return "\n".join(text_parts)

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '../data/exercises')
    output_file = os.path.join(os.path.dirname(__file__), '../exercise_scripts.txt')
    
    module_files = sorted(glob.glob(os.path.join(base_dir, 'module_*.py')))
    
    all_content = []
    
    for file_path in module_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        try:
            tree = ast.parse(source)
        except SyntaxError:
            print(f"Error parsing {file_path}")
            continue
            
        # Find MODULE assignment
        module_node = None
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'MODULE':
                        module_node = node.value
                        break
        
        if not module_node:
            continue
            
        # Extract Module Title
        module_title = "Unknown Module"
        lessons_list = []
        
        for keyword in module_node.keywords:
            if keyword.arg == 'title':
                if isinstance(keyword.value, ast.Constant):
                    module_title = keyword.value.value
            elif keyword.arg == 'lessons':
                if isinstance(keyword.value, ast.List):
                    lessons_list = keyword.value.elts
        
        all_content.append(f"\n\n{'='*40}\n{module_title}\n{'='*40}\n")
        
        for lesson_node in lessons_list:
            if not isinstance(lesson_node, ast.Call):
                continue
                
            lesson_title = "Unknown Lesson"
            example_code = ""
            
            for keyword in lesson_node.keywords:
                if keyword.arg == 'title':
                    if isinstance(keyword.value, ast.Constant):
                        lesson_title = keyword.value.value
                elif keyword.arg == 'example_code':
                    if isinstance(keyword.value, ast.Constant):
                        example_code = keyword.value.value
            
            extracted_text = extract_text_from_code(example_code)
            
            all_content.append(f"\n--- Lección: {lesson_title} ---\n")
            all_content.append(extracted_text)
            all_content.append("\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_content))
    
    print(f"Extraction complete. Saved to {output_file}")

if __name__ == "__main__":
    main()
