from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import io
import traceback

# Change from relative to absolute import
from app.services.orchestrator_service import process_claim
from app.models.schemas import ClaimProcessingResult

app = FastAPI(
    title="HealthPay Claim Processor",
    description="AI-driven system for processing medical insurance claims",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-claim", response_model=ClaimProcessingResult)
async def process_claim_endpoint(files: List[UploadFile] = File(...)):
    """
    Process multiple PDF documents for an insurance claim.
    
    This endpoint:
    1. Accepts multiple PDF files (bill, ID card, discharge summary)
    2. Classifies each document using AI
    3. Extracts and processes information from each document
    4. Validates the extracted data
    5. Returns a structured result with claim decision
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Check file types
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not a PDF")
    
    try:
        # Store file contents in memory with proper BytesIO objects
        file_objects = []
        for file in files:
            contents = await file.read()
            # Create a BytesIO object which has seek() method
            file_obj = io.BytesIO(contents)
            # Add filename attribute to the BytesIO object
            file_obj.filename = file.filename
            file_objects.append(file_obj)
        
        # Process the claim
        result = await process_claim(file_objects)
        return result
    
    except Exception as e:
        # Print detailed error information to the console
        error_details = traceback.format_exc()
        print(f"Error processing claim:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing claim: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)