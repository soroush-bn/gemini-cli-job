import os
import shutil
import subprocess
import sys

# Configuration moved from config.py
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CV_WORKSPACE = os.path.join(SKILL_DIR, "assets")
FACTS_FILE = "facts.txt"
TEMPLATE_NAME = "androidCV.tex"
ML_TEMPLATE_NAME = "MLCV.tex"
OUTPUT_NAME_BASE = "Soroush_Baghernezhad_CV"

def get_career_facts() -> str:
    """Reads the user's career facts and experience from facts.txt."""
    path = os.path.join(CV_WORKSPACE, FACTS_FILE)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Error: facts.txt not found."

def get_cv_template(is_ml: bool = False) -> str:
    """Reads the LaTeX CV template (Android or ML)."""
    filename = ML_TEMPLATE_NAME if is_ml else TEMPLATE_NAME
    path = os.path.join(CV_WORKSPACE, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"Error: Template {filename} not found."

def save_and_compile_latex(latex_content: str, company_name: str, target_dir: str) -> str:
    """
    Saves the full LaTeX content and runs pdflatex to generate a PDF.
    Copies necessary .cls files from the workspace.
    """
    try:
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy .cls files and other assets from CV_WORKSPACE
        for item in os.listdir(CV_WORKSPACE):
            if item.endswith(".cls") or (item.endswith(".tex") and item not in [TEMPLATE_NAME, ML_TEMPLATE_NAME]):
                shutil.copy2(os.path.join(CV_WORKSPACE, item), os.path.join(target_dir, item))

        file_base = f"{OUTPUT_NAME_BASE}_{company_name.replace(' ', '_')}"
        tex_path = os.path.join(target_dir, f"{file_base}.tex")
        pdf_path = os.path.join(target_dir, f"{file_base}.pdf")

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_content)

        # Run pdflatex
        cmd = ["pdflatex", "-interaction=nonstopmode", f"{file_base}.tex"]
        result = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True)

        if os.path.exists(pdf_path):
            return f"Success! CV compiled to {pdf_path}"
        else:
            return f"LaTeX Error: {result.stdout[-1000:]}"

    except Exception as e:
        return f"Error during save/compile: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cv_handler.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "get_facts":
        print(get_career_facts())
    elif command == "get_template":
        is_ml = sys.argv[2].lower() == "true" if len(sys.argv) > 2 else False
        print(get_cv_template(is_ml))
    elif command == "compile":
        if len(sys.argv) < 5:
            print("Usage: python cv_handler.py compile <latex_file_path> <company_name> <target_dir>")
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            content = f.read()
        print(save_and_compile_latex(content, sys.argv[3], sys.argv[4]))
