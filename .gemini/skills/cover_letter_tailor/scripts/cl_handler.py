import os
import sys
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Configuration moved from config.py
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CL_ASSETS = os.path.join(SKILL_DIR, "assets")
TEMPLATE_NAME = "coverletter.docx"
OUTPUT_NAME_BASE = "Soroush_Baghernezhad_Cover_Letter"

def get_coverletter_template() -> str:
    """Reads the text from the docx cover letter template."""
    path = os.path.join(CL_ASSETS, TEMPLATE_NAME)
    if not os.path.exists(path):
        return f"Error: {TEMPLATE_NAME} not found in {CL_ASSETS}."
    
    try:
        doc = Document(path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        return f"Error reading docx: {str(e)}"

def save_coverletter_as_pdf(tailored_text: str, company_name: str, target_dir: str) -> str:
    """
    Saves the tailored text as a PDF in the specified target directory.
    """
    try:
        os.makedirs(target_dir, exist_ok=True)
        
        file_base = f"{OUTPUT_NAME_BASE}_{company_name.replace(' ', '_')}"
        pdf_path = os.path.join(target_dir, f"{file_base}.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        cl_style = ParagraphStyle(
            'CoverLetterStyle',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            spaceAfter=10
        )

        elements = []
        for line in tailored_text.split('\n'):
            if line.strip():
                elements.append(Paragraph(line, cl_style))
            else:
                elements.append(Spacer(1, 12))

        doc.build(elements)

        if os.path.exists(pdf_path):
            return f"Success! Cover Letter saved to {pdf_path}"
        else:
            return "Error: Failed to generate PDF."

    except Exception as e:
        return f"Error during PDF generation: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cl_handler.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "get_template":
        print(get_coverletter_template())
    elif command == "save_pdf":
        if len(sys.argv) < 5:
            print("Usage: python cl_handler.py save_pdf <text_file_path> <company_name> <target_dir>")
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            content = f.read()
        print(save_coverletter_as_pdf(content, sys.argv[3], sys.argv[4]))
