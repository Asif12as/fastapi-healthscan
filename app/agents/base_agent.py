from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAgent(ABC):
    """Base class for document processing agents."""
    
    @abstractmethod
    async def process(self, document_text: str) -> Dict[str, Any]:
        """Process a document and extract structured information."""
        pass
    
    @abstractmethod
    def validate(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Validate the extracted data for completeness and accuracy."""
        pass