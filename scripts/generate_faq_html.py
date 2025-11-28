import json
import os
import markdown

def generate_faq_html():
    json_path = 'public/static/exercises.json'
    output_html = 'public/static/Python_Tutor_FAQ.html'

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
    <title>Python Tutor - Guía de Resolución y FAQ</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; text-align: center; }
        h2 { color: #2980b9; margin-top: 40px; border-bottom: 2px solid #eee; }
        h3 { color: #16a085; margin-top: 30px; }
        .faq-item { background: #f9f9f9; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 20px; border-radius: 0 5px 5px 0; }
        .question { font-weight: bold; color: #e74c3c; margin-bottom: 5px; }
        .answer { margin-bottom: 10px; }
        pre { background: #2d3436; color: #dfe6e9; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: 'Consolas', monospace; }
        .code-block { margin-top: 10px; }
        .page-break { page-break-before: always; }
        .toc { background: #ecf0f1; padding: 20px; border-radius: 5px; margin-bottom: 40px; }
        .toc a { text-decoration: none; color: #2980b9; }
        .toc a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Python Tutor: Guía Maestra de Resolución y FAQ</h1>
    <p style="text-align: center; font-size: 1.2em;">Respuestas, Pistas y Soluciones para todos los ejercicios.</p>
    
    <div class="toc">
        <h2>Índice de Contenidos</h2>
        <ul>
"""

    # Generate TOC
    for i, module in enumerate(data):
        html_content += f'<li><a href="#module-{i}"><strong>{module.get("title", "Módulo")}</strong></a><ul>'
        for lesson in module.get('lessons', []):
            html_content += f'<li><a href="#lesson-{lesson.get("id")}">Ejercicio {lesson.get("id")}: {lesson.get("title")}</a></li>'
        html_content += '</ul></li>'
    
    html_content += """
        </ul>
    </div>
    <div class="page-break"></div>
"""

    # Generate Content
    for i, module in enumerate(data):
        html_content += f'<div id="module-{i}"><h2>{module.get("title", "Módulo")}</h2></div>'
        
        for lesson in module.get('lessons', []):
            title = lesson.get('title', 'Sin Título')
            lid = lesson.get('id')
            content = lesson.get('content', '')
            prompt = lesson.get('exercise_prompt', '')
            hint = lesson.get('hint', '')
            code = lesson.get('example_code', '')

            # Convert markdown content to HTML
            content_html = markdown.markdown(content)

            html_content += f"""
            <div id="lesson-{lid}" class="lesson-section">
                <h3>Ejercicio {lid}: {title}</h3>
                
                <div class="faq-item">
                    <div class="question">Q: ¿De qué trata este ejercicio?</div>
                    <div class="answer">{content_html}</div>
                </div>

                <div class="faq-item">
                    <div class="question">Q: ¿Cuál es el objetivo principal?</div>
                    <div class="answer">{prompt}</div>
                </div>

                <div class="faq-item">
                    <div class="question">Q: Estoy atascado, ¿alguna pista?</div>
                    <div class="answer"><em>{hint}</em></div>
                </div>

                <div class="faq-item">
                    <div class="question">Q: ¿Cómo es la solución o el código de ejemplo?</div>
                    <div class="answer">
                        Aquí tienes el código de referencia para entender la lógica:
                        <div class="code-block">
                            <pre>{code}</pre>
                        </div>
                    </div>
                </div>
                <hr style="border:0; border-top:1px dashed #ccc; margin:30px 0;">
            </div>
            """
        
        html_content += '<div class="page-break"></div>'

    html_content += """
</body>
</html>
"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML generated: {output_html}")

if __name__ == "__main__":
    generate_faq_html()
