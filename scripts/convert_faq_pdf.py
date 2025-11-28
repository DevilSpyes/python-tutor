import sys
from weasyprint import HTML

def convert_faq_to_pdf():
    html_path = 'public/static/Python_Tutor_FAQ.html'
    pdf_path = 'Python_Tutor_FAQ.pdf'
    
    print(f"Converting {html_path} to {pdf_path}...")
    try:
        HTML(html_path).write_pdf(pdf_path)
        print("Conversion successful!")
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert_faq_to_pdf()
