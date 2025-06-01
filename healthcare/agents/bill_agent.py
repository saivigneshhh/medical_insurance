# agents/bill_agent.py
from ..ai_client import LLMClient # Note the '..'
from ..schemas import BillData # Note the '..'
from typing import Dict, Any

class BillAgent:
    """
    Agent responsible for extracting structured data from medical bill text using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def process(self, bill_text: str) -> BillData:
        """
        Extracts specific fields from the bill text and structures them into a BillData object.
        """
        # Define the JSON schema for the desired output
        bill_schema = {
            "type": "object",
            "properties": {
                "hospital_name": {"type": "string", "description": "Name of the hospital."},
                "total_amount": {"type": "number", "description": "Total amount of the bill."},
                "date_of_service": {"type": "string", "format": "date", "description": "Date of service in YYYY-MM-DD format."}
            },
            "required": ["hospital_name", "total_amount", "date_of_service"],
            "propertyOrdering": ["hospital_name", "total_amount", "date_of_service"]
        }

        prompt = f"""
        Extract the following information from the provided medical bill text and return it as a JSON object:
        - Hospital Name
        - Total Amount
        - Date of Service (in YYYY-MM-DD format)

        If a field is not found, use null.

        Medical Bill Text:
        {bill_text}
        """
        try:
            extracted_data = await self.llm_client.generate_structured_json(prompt, bill_schema)
            return BillData(**extracted_data)
        except ValidationError as e:
            print(f"Validation error for BillData: {e}")
            return BillData(
                hospital_name=None,
                total_amount=None,
                date_of_service=None
            )
        except Exception as e:
            print(f"Error processing bill with LLM: {e}")
            return BillData(
                hospital_name=None,
                total_amount=None,
                date_of_service=None
            )