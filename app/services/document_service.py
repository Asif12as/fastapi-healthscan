from typing import List, Dict, Any, BinaryIO
from ..utils.pdf_utils import process_pdf_files
from ..utils.llm_utils import classify_document_with_gemini

async def process_documents(files: List[BinaryIO]) -> List[Dict[str, Any]]:
    """
    Process uploaded documents:
    1. Extract text from PDFs
    2. Classify documents by type
    """
    # Extract text from PDFs
    documents = await process_pdf_files(files)
    
    # Classify each document
    for doc in documents:
        doc_type = await classify_document_with_gemini(doc["content"], doc["filename"])
        doc["type"] = doc_type
    
    return documents