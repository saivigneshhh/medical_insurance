# agents/validation_agent.py
from typing import List
from ..schemas import ProcessedDocument, ValidationResult, DocumentType, BillData, DischargeSummaryData # Note the '..'

class ValidationAgent:
    """
    Agent responsible for validating the extracted data and checking for inconsistencies.
    """
    async def validate(self, processed_documents: List[ProcessedDocument]) -> ValidationResult:
        """
        Performs validation checks on the processed documents.
        """
        missing_docs = []
        discrepancies = []

        # Check for required documents
        doc_types_present = {doc.type for doc in processed_documents}
        
        # For a basic claim, we might require at least a bill and a discharge summary
        required_types = {DocumentType.BILL, DocumentType.DISCHARGE_SUMMARY}
        for req_type in required_types:
            if req_type not in doc_types_present:
                missing_docs.append(req_type.value)

        # Gather data for cross-checking
        bill_data: List[BillData] = [
            doc.data for doc in processed_documents
            if doc.type == DocumentType.BILL and isinstance(doc.data, BillData)
        ]
        discharge_data: List[DischargeSummaryData] = [
            doc.data for doc in processed_documents
            if doc.type == DocumentType.DISCHARGE_SUMMARY and isinstance(doc.data, DischargeSummaryData)
        ]

        # Perform cross-checks
        if bill_data and discharge_data:
            # Simple check: patient name consistency (if available in bill, which is rare)
            # For this example, we'll focus on dates and general presence
            
            # Example: Check if discharge date from summary is after admission date
            for ds in discharge_data:
                if ds.admission_date and ds.discharge_date:
                    try:
                        # Basic string comparison for YYYY-MM-DD should work for order
                        if ds.discharge_date < ds.admission_date:
                            discrepancies.append(f"Discharge date ({ds.discharge_date}) is before admission date ({ds.admission_date}) in discharge summary.")
                    except Exception:
                        discrepancies.append(f"Invalid date format in discharge summary: Admission={ds.admission_date}, Discharge={ds.discharge_date}.")

        # Check for missing critical fields within extracted data
        for doc in processed_documents:
            if doc.type == DocumentType.BILL and isinstance(doc.data, BillData):
                if not doc.data.hospital_name: discrepancies.append(f"Missing hospital name in bill document: {doc.filename}")
                if not doc.data.total_amount: discrepancies.append(f"Missing total amount in bill document: {doc.filename}")
                if not doc.data.date_of_service: discrepancies.append(f"Missing date of service in bill document: {doc.filename}")
            elif doc.type == DocumentType.DISCHARGE_SUMMARY and isinstance(doc.data, DischargeSummaryData):
                if not doc.data.patient_name: discrepancies.append(f"Missing patient name in discharge summary: {doc.filename}")
                if not doc.data.diagnosis: discrepancies.append(f"Missing diagnosis in discharge summary: {doc.filename}")
                if not doc.data.admission_date: discrepancies.append(f"Missing admission date in discharge summary: {doc.filename}")
                if not doc.data.discharge_date: discrepancies.append(f"Missing discharge date in discharge summary: {doc.filename}")

        return ValidationResult(
            missing_documents=list(set(missing_docs)), # Use set to remove duplicates
            discrepancies=list(set(discrepancies))
        )