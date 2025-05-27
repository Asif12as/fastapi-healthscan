from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import date

class BillDocument(BaseModel):
    type: Literal["bill"] = "bill"
    hospital_name: str
    total_amount: float
    date_of_service: date

class DischargeDocument(BaseModel):
    type: Literal["discharge_summary"] = "discharge_summary"
    patient_name: str
    diagnosis: str
    admission_date: date
    discharge_date: date

class IdCardDocument(BaseModel):
    type: Literal["id_card"] = "id_card"
    patient_name: str
    insurance_id: str
    plan_name: str
    expiration_date: Optional[date] = None

# Union type for all document types
Document = BillDocument | DischargeDocument | IdCardDocument

class ValidationResult(BaseModel):
    missing_documents: List[str] = Field(default_factory=list)
    discrepancies: List[str] = Field(default_factory=list)

class ClaimDecision(BaseModel):
    status: Literal["approved", "rejected"]
    reason: str

class ClaimProcessingResult(BaseModel):
    documents: List[Document]
    validation: ValidationResult
    claim_decision: ClaimDecision