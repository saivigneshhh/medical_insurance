# pdf_parser.py
from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text from a PDF file's binary content.
    Assumes the PDF is text-based and not an image-only PDF.
    """
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or "" # Use .extract_text() and handle None
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise ValueError(f"Could not extract text from PDF: {e}")