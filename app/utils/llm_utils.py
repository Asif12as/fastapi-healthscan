import os
import json
from typing import Any, Dict, List, Optional
import google.generativeai as genai
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API keys
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def classify_document_with_gemini(text: str, filename: str) -> str:
    """Classify a document based on its content and filename using Google Gemini."""
    prompt = f"""
    Analyze the following document content and filename to determine the document type.
    Classify it as one of: 'bill', 'discharge_summary', 'id_card'.
    
    Filename: {filename}
    
    Document content snippet:
    {text[:500]}...
    
    Return only the document type as a single word (bill, discharge_summary, or id_card).
    """
    
    # Updated model initialization to handle API version compatibility
    try:
        # Use the correct model name format for the current API version
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = await model.generate_content_async(prompt)
        document_type = response.text.strip().lower()
    except Exception as e:
        error_message = str(e)
        print(f"Error with Gemini API: {error_message}")
        
        # Check for specific error types
        if "429" in error_message or "quota" in error_message.lower() or "rate limit" in error_message.lower():
            print("Rate limit or quota exceeded. Using fallback classification.")
        elif "404" in error_message:
            print("Model not found. Check if the model name is correct.")
        
        # Fallback classification based on filename if API fails
        if "bill" in filename.lower():
            return "bill"
        elif "discharge" in filename.lower() or "summary" in filename.lower():
            return "discharge_summary"
        elif "id" in filename.lower() or "card" in filename.lower():
            return "id_card"
        else:
            return "unknown"
    
    # Normalize response
    if "bill" in document_type:
        return "bill"
    elif "discharge" in document_type or "summary" in document_type:
        return "discharge_summary"
    elif "id" in document_type or "card" in document_type:
        return "id_card"
    else:
        return "unknown"

async def extract_structured_data_with_gpt(document_type: str, text: str) -> Dict[str, Any]:
    """Extract structured data from text based on document type using GPT."""
    
    prompt_templates = {
        "bill": """
        Extract the following information from this medical bill:
        - Hospital name
        - Total amount
        - Date of service (in YYYY-MM-DD format)
        
        Bill text:
        {text}
        
        Return the information in JSON format.
        """,
        
        "discharge_summary": """
        Extract the following information from this hospital discharge summary:
        - Patient name
        - Diagnosis
        - Admission date (in YYYY-MM-DD format)
        - Discharge date (in YYYY-MM-DD format)
        
        Discharge summary text:
        {text}
        
        Return the information in JSON format.
        """,
        
        "id_card": """
        Extract the following information from this insurance ID card:
        - Patient name
        - Insurance ID
        - Plan name
        - Expiration date (in YYYY-MM-DD format, if available)
        
        ID card text:
        {text}
        
        Return the information in JSON format.
        """
    }
    
    prompt = prompt_templates.get(document_type, "").format(text=text)
    
    response = await openai_client.chat.completions.create(
        model="gpt-4o mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured data from medical documents."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    result["type"] = document_type
    return result