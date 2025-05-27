from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..utils.llm_utils import extract_structured_data_with_gpt

class BillAgent(BaseAgent):
    """Agent for processing medical bills."""
    
    async def process(self, document_text: str) -> Dict[str, Any]:
        """Extract structured data from a medical bill."""
        return await extract_structured_data_with_gpt("bill", document_text)
    
    def validate(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Validate bill data for completeness and accuracy."""
        issues = []
        
        required_fields = ["hospital_name", "total_amount", "date_of_service"]
        for field in required_fields:
            if field not in extracted_data or not extracted_data[field]:
                issues.append(f"Missing {field} in bill document")
        
        if "total_amount" in extracted_data:
            try:
                amount = float(extracted_data["total_amount"])
                if amount <= 0:
                    issues.append("Bill amount must be greater than zero")
            except (ValueError, TypeError):
                issues.append("Invalid bill amount format")
        
        return issues