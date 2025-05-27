from typing import Dict, Any, List, Tuple
from ..models.schemas import ValidationResult, ClaimDecision

def validate_claim_documents(structured_documents: List[Dict[str, Any]]) -> Tuple[ValidationResult, ClaimDecision]:
    """
    Validate the claim by:
    1. Checking for required document types
    2. Checking for data consistency across documents
    3. Making a claim decision based on validation results
    """
    # Initialize validation result
    validation_result = ValidationResult()
    
    # Check for required document types
    required_types = ["bill", "discharge_summary", "id_card"]
    found_types = [doc["type"] for doc in structured_documents]
    
    missing_types = [req_type for req_type in required_types if req_type not in found_types]
    validation_result.missing_documents = missing_types
    
    # Collect all validation issues from individual documents
    for doc in structured_documents:
        if "validation_issues" in doc and doc["validation_issues"]:
            for issue in doc["validation_issues"]:
                validation_result.discrepancies.append(f"{doc['type']}: {issue}")
    
    # Check for cross-document consistency
    if "bill" in found_types and "discharge_summary" in found_types:
        bill = next(doc for doc in structured_documents if doc["type"] == "bill")
        discharge = next(doc for doc in structured_documents if doc["type"] == "discharge_summary")
        
        # Check if service date matches discharge date
        if bill.get("date_of_service") != discharge.get("discharge_date"):
            validation_result.discrepancies.append(
                "Bill service date does not match discharge date"
            )
    
    if "id_card" in found_types and "discharge_summary" in found_types:
        id_card = next(doc for doc in structured_documents if doc["type"] == "id_card")
        discharge = next(doc for doc in structured_documents if doc["type"] == "discharge_summary")
        
        # Check if patient names match
        if id_card.get("patient_name") != discharge.get("patient_name"):
            validation_result.discrepancies.append(
                "Patient name on ID card does not match discharge summary"
            )
    
    # Make claim decision
    claim_decision = make_claim_decision(validation_result)
    
    return validation_result, claim_decision

def make_claim_decision(validation: ValidationResult) -> ClaimDecision:
    """Determine if a claim should be approved or rejected based on validation results."""
    if validation.missing_documents or validation.discrepancies:
        return ClaimDecision(
            status="rejected",
            reason=format_rejection_reason(validation)
        )
    else:
        return ClaimDecision(
            status="approved",
            reason="All required documents present and data is consistent"
        )

def format_rejection_reason(validation: ValidationResult) -> str:
    """Format a human-readable rejection reason based on validation issues."""
    reasons = []
    
    if validation.missing_documents:
        missing_docs = ", ".join(validation.missing_documents)
        reasons.append(f"Missing required documents: {missing_docs}")
    
    if validation.discrepancies:
        reasons.append("Data discrepancies found: " + "; ".join(validation.discrepancies))
    
    return " ".join(reasons)