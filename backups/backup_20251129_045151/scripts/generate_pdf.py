
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

def generate_pdf():
    json_path = 'public/static/exercises.json'
    output_pdf = 'Python_Tutor_Curriculum.pdf'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    doc = SimpleDocTemplate(output_pdf, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    Story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    if 'Code' not in styles:
        styles.add(ParagraphStyle(name='Code',
                                  parent=styles['Normal'],
                                  fontName='Courier',
                                  fontSize=8,
                                  leading=10,
                                  textColor=colors.black,
                                  backColor=colors.whitesmoke,
                                  borderPadding=5))

    styles.add(ParagraphStyle(name='ModuleTitle',
                              parent=styles['Heading1'],
                              fontSize=18,
                              spaceAfter=12))

    styles.add(ParagraphStyle(name='LessonTitle',
                              parent=styles['Heading2'],
                              fontSize=14,
                              spaceBefore=12,
                              spaceAfter=6))

    # Title Page
    Story.append(Paragraph("Python Tutor Curriculum", styles['Title']))
    Story.append(Spacer(1, 12))
    Story.append(Paragraph("Generated automatically from Python Tutor", styles['Normal']))
    Story.append(PageBreak())

    for module in data:
        module_title = module.get('title', 'Untitled Module')
        Story.append(Paragraph(module_title, styles['ModuleTitle']))
        Story.append(Spacer(1, 12))

        lessons = module.get('lessons', [])
        for lesson in lessons:
            lesson_title = lesson.get('title', 'Untitled Lesson')
            Story.append(Paragraph(lesson_title, styles['LessonTitle']))
            
            content = lesson.get('content', '')
            if content:
                # Basic markdown cleaning/formatting for ReportLab
                # ReportLab supports some XML tags like <b>, <i>
                # We'll just replace newlines with <br/> for now and escape basic chars if needed
                formatted_content = content.replace('\n', '<br/>')
                Story.append(Paragraph(formatted_content, styles['Normal']))
                Story.append(Spacer(1, 6))

            example_code = lesson.get('example_code', '')
            if example_code:
                Story.append(Paragraph("<b>Example Code:</b>", styles['Normal']))
                Story.append(Preformatted(example_code, styles['Code']))
                Story.append(Spacer(1, 12))
        
        Story.append(PageBreak())

    doc.build(Story)
    print(f"PDF generated successfully: {output_pdf}")

if __name__ == "__main__":
    generate_pdf()
