# orchestrator.py
import asyncio
from typing import List
from fastapi import UploadFile

from ai_client import LLMClient
from pdf_parser import extract_text_from_pdf
from schemas import (
    DocumentType, ProcessedDocument, ClaimProcessingResponse,
    BillData, DischargeSummaryData, ValidationResult, ClaimDecision
)
from agents.document_classifier_agent import DocumentClassifierAgent
from agents.text_extraction_agent import TextExtractionAgent
from agents.bill_agent import BillAgent
from agents.discharge_agent import DischargeAgent
from agents.validation_agent import ValidationAgent
from agents.claim_decision_agent import ClaimDecisionAgent

class ClaimOrchestrator:
    """
    Orchestrates the entire claim processing pipeline, managing the flow between different agents.
    """
    def __init__(self):
        self.llm_client = LLMClient()
        self.text_extraction_agent = TextExtractionAgent()
        self.document_classifier_agent = DocumentClassifierAgent(self.llm_client)
        self.bill_agent = BillAgent(self.llm_client)
        self.discharge_agent = DischargeAgent(self.llm_client)
        self.validation_agent = ValidationAgent()
        self.claim_decision_agent = ClaimDecisionAgent()

    async def _process_single_document(self, file: UploadFile) -> ProcessedDocument:
        """
        Processes a single uploaded document through text extraction, classification,
        and structured data extraction.
        """
        filename = file.filename if file.filename else "unknown_file"
        print(f"Processing document: {filename}")

        # 1. Extract raw text from PDF
        raw_text = await self.text_extraction_agent.extract(file)
        
        # 2. Classify the document type
        doc_type = await self.document_classifier_agent.classify(raw_text, filename)
        
        structured_data = None
        if doc_type == DocumentType.BILL:
            structured_data = await self.bill_agent.process(raw_text)
        elif doc_type == DocumentType.DISCHARGE_SUMMARY:
            structured_data = await self.discharge_agent.process(raw_text)
        # Add more conditions for other document types like ID_CARD if needed
        
        return ProcessedDocument(
            type=doc_type,
            data=structured_data,
            raw_text=raw_text,
            filename=filename
        )

    async def process_claim(self, files: List[UploadFile]) -> ClaimProcessingResponse:
        """
        Main method to process multiple claim documents.
        """
        if not files:
            raise ValueError("No files provided for claim processing.")

        # Process each document concurrently
        processing_tasks = [self._process_single_document(file) for file in files]
        processed_documents: List[ProcessedDocument] = await asyncio.gather(*processing_tasks)

        # 3. Validate the extracted data
        validation_result: ValidationResult = await self.validation_agent.validate(processed_documents)

        # 4. Make a final claim decision
        claim_decision: ClaimDecision = await self.claim_decision_agent.decide(validation_result)

        return ClaimProcessingResponse(
            documents=processed_documents,
            validation=validation_result,
            claim_decision=claim_decision
        )