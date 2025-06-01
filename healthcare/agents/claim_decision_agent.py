# agents/claim_decision_agent.py
from ..schemas import ValidationResult, ClaimDecision # Note the '..'

class ClaimDecisionAgent:
    """
    Agent responsible for making the final claim decision (approve/reject)
    based on the validation results.
    """
    async def decide(self, validation_result: ValidationResult) -> ClaimDecision:
        """
        Determines the claim status and reason.
        """
        if validation_result.missing_documents or validation_result.discrepancies:
            status = "rejected"
            reasons = []
            if validation_result.missing_documents:
                reasons.append(f"Missing required documents: {', '.join(validation_result.missing_documents)}.")
            if validation_result.discrepancies:
                reasons.append(f"Discrepancies found: {'; '.join(validation_result.discrepancies)}.")
            reason = " ".join(reasons)
        else:
            status = "approved"
            reason = "All required documents present and data is consistent."

        return ClaimDecision(status=status, reason=reason)