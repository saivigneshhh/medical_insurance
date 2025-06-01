# schemas.py
import enum
from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError

# Define an Enum for document types
class DocumentType(str, enum.Enum):
    """Enum for classifying different types of medical claim documents."""
    BILL = "bill"
    ID_CARD = "id_card"
    DISCHARGE_SUMMARY = "discharge_summary"
    UNKNOWN = "unknown"

# Define Pydantic models for structured data extracted from documents
class BillData(BaseModel):
    """Schema for data extracted from a medical bill."""
    hospital_name: Optional[str] = Field(None, description="Name of the hospital.")
    total_amount: Optional[float] = Field(None, description="Total amount of the bill.")
    date_of_service: Optional[str] = Field(None, description="Date of service in YYYY-MM-DD format.")

class DischargeSummaryData(BaseModel):
    """Schema for data extracted from a discharge summary."""
    patient_name: Optional[str] = Field(None, description="Name of the patient.")
    diagnosis: Optional[str] = Field(None, description="Medical diagnosis.")
    admission_date: Optional[str] = Field(None, description="Date of admission in YYYY-MM-DD format.")
    discharge_date: Optional[str] = Field(None, description="Date of discharge in YYYY-MM-DD format.")

# A union type for the data field in ProcessedDocument, allowing different structured data types
DocumentSpecificData = Union[BillData, DischargeSummaryData]

class ProcessedDocument(BaseModel):
    """Schema for a single processed document, including its type and extracted structured data."""
    type: DocumentType = Field(..., description="The classified type of the document.")
    data: Optional[DocumentSpecificData] = Field(None, description="Structured data extracted from the document.")
    raw_text: str = Field(..., description="The raw text extracted from the PDF document.")
    filename: str = Field(..., description="The original filename of the document.")

class ValidationResult(BaseModel):
    """Schema for the validation outcome of all processed documents."""
    missing_documents: List[str] = Field(..., description="List of document types that are expected but missing.")
    discrepancies: List[str] = Field(..., description="List of inconsistencies or errors found in the data.")

class ClaimDecision(BaseModel):
    """Schema for the final claim decision."""
    status: str = Field(..., description="The status of the claim (e.g., 'approved', 'rejected').")
    reason: str = Field(..., description="The reason for the claim decision.")

class ClaimProcessingResponse(BaseModel):
    """Overall response schema for the claim processing endpoint."""
    documents: List[ProcessedDocument] = Field(..., description="List of all processed documents with their extracted data.")
    validation: ValidationResult = Field(..., description="Result of the validation checks.")
    claim_decision: ClaimDecision = Field(..., description="The final decision regarding the claim.")