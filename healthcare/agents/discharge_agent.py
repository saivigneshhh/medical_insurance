# agents/discharge_agent.py
from ..ai_client import LLMClient # Note the '..'
from ..schemas import DischargeSummaryData # Note the '..'
from typing import Dict, Any

class DischargeAgent:
    """
    Agent responsible for extracting structured data from discharge summary text using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def process(self, discharge_text: str) -> DischargeSummaryData:
        """
        Extracts specific fields from the discharge summary text and structures them into a DischargeSummaryData object.
        """
        # Define the JSON schema for the desired output
        discharge_schema = {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string", "description": "Name of the patient."},
                "diagnosis": {"type": "string", "description": "Medical diagnosis."},
                "admission_date": {"type": "string", "format": "date", "description": "Date of admission in YYYY-MM-DD format."},
                "discharge_date": {"type": "string", "format": "date", "description": "Date of discharge in YYYY-MM-DD format."}
            },
            "required": ["patient_name", "diagnosis", "admission_date", "discharge_date"],
            "propertyOrdering": ["patient_name", "diagnosis", "admission_date", "discharge_date"]
        }

        prompt = f"""
        Extract the following information from the provided discharge summary text and return it as a JSON object:
        - Patient Name
        - Diagnosis
        - Admission Date (in YYYY-MM-DD format)
        - Discharge Date (in YYYY-MM-DD format)

        If a field is not found, use null.

        Discharge Summary Text:
        {discharge_text}
        """
        try:
            extracted_data = await self.llm_client.generate_structured_json(prompt, discharge_schema)
            return DischargeSummaryData(**extracted_data)
        except ValidationError as e:
            print(f"Validation error for DischargeSummaryData: {e}")
            return DischargeSummaryData(
                patient_name=None,
                diagnosis=None,
                admission_date=None,
                discharge_date=None
            )
        except Exception as e:
            print(f"Error processing discharge summary with LLM: {e}")
            return DischargeSummaryData(
                patient_name=None,
                diagnosis=None,
                admission_date=None,
                discharge_date=None
            )