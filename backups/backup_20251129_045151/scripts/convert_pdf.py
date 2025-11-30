import sys
from weasyprint import HTML

def convert_html_to_pdf(html_path, pdf_path):
    print(f"Converting {html_path} to {pdf_path}...")
    try:
        HTML(html_path).write_pdf(pdf_path)
        print("Conversion successful!")
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_html_to_pdf('public/static/Python_Tutor_Curriculum.html', 'Python_Tutor_Curriculum.pdf')
