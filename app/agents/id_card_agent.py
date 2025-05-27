from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..utils.llm_utils import extract_structured_data_with_gpt
from datetime import datetime

class IdCardAgent(BaseAgent):
    """Agent for processing insurance ID cards."""
    
    async def process(self, document_text: str) -> Dict[str, Any]:
        """Extract structured data from an insurance ID card."""
        return await extract_structured_data_with_gpt("id_card", document_text)
    
    def validate(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Validate ID card data for completeness and accuracy."""
        issues = []
        
        required_fields = ["patient_name", "insurance_id", "plan_name"]
        for field in required_fields:
            if field not in extracted_data or not extracted_data[field]:
                issues.append(f"Missing {field} in ID card")
        
        # Validate expiration date if provided
        if "expiration_date" in extracted_data and extracted_data["expiration_date"]:
            try:
                expiration = datetime.fromisoformat(str(extracted_data["expiration_date"]))
                today = datetime.now()
                
                if expiration < today:
                    issues.append("Insurance ID card is expired")
            except (ValueError, TypeError):
                issues.append("Invalid expiration date format in ID card")
        
        return issues