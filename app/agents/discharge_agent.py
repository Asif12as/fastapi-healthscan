from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..utils.llm_utils import extract_structured_data_with_gpt
from datetime import datetime

class DischargeAgent(BaseAgent):
    """Agent for processing hospital discharge summaries."""
    
    async def process(self, document_text: str) -> Dict[str, Any]:
        """Extract structured data from a discharge summary."""
        return await extract_structured_data_with_gpt("discharge_summary", document_text)
    
    def validate(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Validate discharge summary data for completeness and accuracy."""
        issues = []
        
        required_fields = ["patient_name", "diagnosis", "admission_date", "discharge_date"]
        for field in required_fields:
            if field not in extracted_data or not extracted_data[field]:
                issues.append(f"Missing {field} in discharge summary")
        
        # Validate admission date is before discharge date
        if "admission_date" in extracted_data and "discharge_date" in extracted_data:
            try:
                admission = datetime.fromisoformat(str(extracted_data["admission_date"]))
                discharge = datetime.fromisoformat(str(extracted_data["discharge_date"]))
                
                if admission > discharge:
                    issues.append("Admission date cannot be after discharge date")
            except (ValueError, TypeError):
                issues.append("Invalid date format in discharge summary")
        
        return issues