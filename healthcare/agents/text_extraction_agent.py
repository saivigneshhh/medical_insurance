# agents/text_extraction_agent.py
from fastapi import UploadFile
from ..pdf_parser import extract_text_from_pdf # Note the '..'

class TextExtractionAgent:
    """
    Agent responsible for extracting raw text content from PDF files.
    This agent uses a PDF parsing library, not an LLM, for raw text extraction.
    """
    async def extract(self, pdf_file: UploadFile) -> str:
        """
        Extracts all readable text from the provided PDF file.
        """
        try:
            file_content = await pdf_file.read()
            extracted_text = extract_text_from_pdf(file_content)
            return extracted_text
        except Exception as e:
            print(f"Error in TextExtractionAgent: {e}")
            raise ValueError(f"Failed to extract text from PDF: {pdf_file.filename}. Error: {e}")