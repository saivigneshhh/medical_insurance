# agents/document_classifier_agent.py
from typing import Literal
from ..ai_client import LLMClient # Note the '..'
from ..schemas import DocumentType # Note the '..'

class DocumentClassifierAgent:
    """
    Agent responsible for classifying the type of a document (e.g., bill, discharge summary)
    based on its content and filename using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def classify(self, text_content: str, filename: str) -> DocumentType:
        """
        Classifies the document type.
        """
        prompt = f"""
        Given the following document content and filename, classify the document into one of these types:
        'bill', 'id_card', 'discharge_summary', 'unknown'.
        
        Document Content (first 500 characters):
        {text_content[:500]}
        
        Filename: {filename}
        
        Return only the classified type string (e.g., 'bill').
        """
        
        try:
            classification_str = await self.llm_client.generate_text(prompt)
            classification_str = classification_str.strip().lower().replace("'", "")
            
            if classification_str in [dt.value for dt in DocumentType]:
                return DocumentType(classification_str)
            else:
                print(f"LLM returned an unrecognized document type: {classification_str}. Defaulting to UNKNOWN.")
                return DocumentType.UNKNOWN
        except Exception as e:
            print(f"Error classifying document with LLM: {e}")
            return DocumentType.UNKNOWN