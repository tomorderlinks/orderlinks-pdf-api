import base64
import io
import pdfplumber

def extract_text_from_base64_pdf(base64_string: str) -> str:
    missing = len(base64_string) % 4
    if missing:
        base64_string += "=" * (4 - missing)

    pdf_bytes = base64.b64decode(base64_string)
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text.strip()

def extract_text_from_file_bytes(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text.strip()

def run(payload: dict):
    if payload.get("text"):
        return extract_text_from_base64_pdf(payload["text"])
    if payload.get("file_bytes"):
        return extract_text_from_file_bytes(payload["file_bytes"])
    raise ValueError("No valid input provided")