import os
from pypdf import PdfReader
from typing import List, Dict, Any, BinaryIO
import io

async def extract_text_from_pdf(file_content: BinaryIO) -> str:
    """Extract text content from a PDF file."""
    try:
        # Make sure the file pointer is at the beginning
        file_content.seek(0)
        pdf_reader = PdfReader(file_content)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return "Error extracting text"

async def process_pdf_files(files: List[BinaryIO]) -> List[Dict[str, Any]]:
    """Process multiple PDF files and extract their text content."""
    results = []
    for file in files:
        text = await extract_text_from_pdf(file)
        results.append({
            "filename": getattr(file, "filename", "unknown"),
            "content": text
        })
    return results