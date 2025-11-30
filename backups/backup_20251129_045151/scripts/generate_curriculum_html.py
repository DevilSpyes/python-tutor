
import json
import os
import html

def generate_html():
    json_path = '../public/static/exercises_v2.json'
    output_html = 'Python_Tutor_Curriculum.html'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Tutor Curriculum</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            margin-top: 40px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }
        .module {
            margin-bottom: 60px;
        }
        .lesson {
            margin-bottom: 40px;
        }
        .toc {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 40px;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin-bottom: 5px;
        }
        .toc a {
            text-decoration: none;
            color: #3498db;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        @media print {
            body {
                max-width: 100%;
                padding: 0;
            }
            .page-break {
                page-break-before: always;
            }
            a {
                text-decoration: none;
                color: #000;
            }
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
        }
    </style>
</head>
<body>
    <div class="cover">
        <h1 style="text-align: center; margin-top: 200px; font-size: 3em;">Python Tutor</h1>
        <h2 style="text-align: center; color: #7f8c8d;">Curriculum Completo</h2>
        <p style="text-align: center; margin-top: 50px;">Generado automáticamente</p>
    </div>
    
    <div class="page-break"></div>

    <div class="toc">
        <h2>Tabla de Contenidos</h2>
        <ul>
"""

    # Generate TOC
    for module in data:
        module_title = html.escape(module.get('title', 'Untitled Module'))
        module_id = f"module-{module.get('id', 0)}"
        html_content += f'<li><a href="#{module_id}"><strong>{module_title}</strong></a><ul>'
        
        for lesson in module.get('lessons', []):
            lesson_title = html.escape(lesson.get('title', 'Untitled Lesson'))
            lesson_id = f"lesson-{lesson.get('id', 0)}"
            html_content += f'<li><a href="#{lesson_id}">{lesson_title}</a></li>'
        
        html_content += '</ul></li>'

    html_content += """
        </ul>
    </div>

    <div class="page-break"></div>
"""

    # Generate Content
    for module in data:
        module_title = html.escape(module.get('title', 'Untitled Module'))
        module_id = f"module-{module.get('id', 0)}"
        
        html_content += f'<div class="module" id="{module_id}">'
        html_content += f'<h1>{module_title}</h1>'
        
        for lesson in module.get('lessons', []):
            lesson_title = html.escape(lesson.get('title', 'Untitled Lesson'))
            lesson_id = f"lesson-{lesson.get('id', 0)}"
            content = html.escape(lesson.get('content', '')).replace('\n', '<br>')
            example_code = html.escape(lesson.get('example_code', ''))
            
            html_content += f'<div class="lesson" id="{lesson_id}">'
            html_content += f'<h2>{lesson_title}</h2>'
            
            if content:
                html_content += f'<div class="content"><p>{content}</p></div>'
            
            if example_code:
                html_content += f'<h3>Código de Ejemplo</h3>'
                html_content += f'<pre>{example_code}</pre>'
            
            html_content += '</div>'
            html_content += '<hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">'
        
        html_content += '</div><div class="page-break"></div>'

    html_content += """
</body>
</html>
"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML generated successfully: {output_html}")

if __name__ == "__main__":
    generate_html()
