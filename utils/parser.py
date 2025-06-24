import docx2txt
import fitz  # PyMuPDF

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "".join(page.get_text() for page in doc)
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""
