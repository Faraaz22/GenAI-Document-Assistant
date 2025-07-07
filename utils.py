import fitz  # PyMuPDF

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
