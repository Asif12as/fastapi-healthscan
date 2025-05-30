# HealthPay - AI-Driven Medical Insurance Claims Processor

HealthPay is an advanced system for processing medical insurance claims using AI technologies. It automates the analysis of medical documents, extracts relevant information, and makes claim decisions based on document validation.

## Architecture & Logic

### System Overview

HealthPay is built as a microservice-based application with a FastAPI backend. The system follows a document-processing workflow architecture with specialized agents for different document types.

### Core Components 

1. **API Layer** (`app/main.py`)
   - Provides RESTful endpoints for claim processing
   - Handles document uploads and validation
   - Returns structured claim processing results

2. **Orchestration Service** (`app/services/orchestrator_service.py`)
   - Implements a directed workflow graph using LangGraph
   - Manages the sequential processing of documents through various stages
   - Coordinates between different services and agents

3. **Document Service** (`app/services/document_service.py`)
   - Processes PDF documents to extract text content
   - Uses AI to classify documents by type (bill, ID card, discharge summary)

4. **Agent-Based Processing** (`app/agents/`)
   - Implements specialized agents for each document type:
     - `BillAgent`: Processes medical bills
     - `DischargeAgent`: Processes hospital discharge summaries
     - `IdCardAgent`: Processes insurance ID cards
   - Each agent extracts structured data and validates document-specific information

5. **Validation Service** (`app/services/validation_service.py`)
   - Validates claim documents for completeness and consistency
   - Checks for cross-document data consistency
   - Makes claim decisions based on validation results

### Processing Workflow

1. **Document Upload**: System receives PDF documents through the API
2. **Text Extraction**: PDF content is extracted using PyPDF
3. **Document Classification**: AI classifies each document by type
4. **Information Extraction**: Specialized agents extract structured data from each document
5. **Validation**: System validates document completeness and data consistency
6. **Decision Making**: Based on validation results, the system approves or rejects the claim
7. **Result Formatting**: Final results are formatted and returned to the client

## AI Integration

HealthPay leverages multiple AI models for different tasks in the processing pipeline:

### Google Gemini

Google's Gemini model is used for document classification. The system sends document content and filename to the Gemini API, which analyzes the text and determines the document type (bill, discharge summary, or ID card).

**Integration Point**: `app/utils/llm_utils.py` - `classify_document_with_gemini()` function

### OpenAI GPT-4

GPT-4 is used for structured information extraction from documents. Each document type has a specialized prompt that instructs the model to extract specific fields in a structured JSON format.

**Integration Point**: `app/utils/llm_utils.py` - `extract_structured_data_with_gpt()` function

### Fallback Mechanisms

The system includes fallback mechanisms for AI service failures:
- If the Gemini API fails, the system attempts to classify documents based on filename patterns
- Error handling captures and logs AI service issues for debugging

## AI Prompt Examples

### Document Classification Prompt (Gemini)

```
Analyze the following document content and filename to determine the document type.
Classify it as one of: 'bill', 'discharge_summary', 'id_card'.

Filename: {filename}

Document content snippet:
{text[:500]}...

Return only the document type as a single word (bill, discharge_summary, or id_card).
```

### Medical Bill Information Extraction Prompt (GPT-4)

```
Extract the following information from this medical bill:
- Hospital name
- Total amount
- Date of service (in YYYY-MM-DD format)

Bill text:
{text}

Return the information in JSON format.
```

### Discharge Summary Information Extraction Prompt (GPT-4)

```
Extract the following information from this hospital discharge summary:
- Patient name
- Diagnosis
- Admission date (in YYYY-MM-DD format)
- Discharge date (in YYYY-MM-DD format)

Discharge summary text:
{text}

Return the information in JSON format.
```

## Technical Stack

- **Backend Framework**: FastAPI
- **AI Services**: Google Generative AI (Gemini), OpenAI GPT-4
- **PDF Processing**: PyPDF
- **Workflow Management**: LangGraph
- **Data Validation**: Pydantic
- **Testing**: Pytest

## Getting Started

### Prerequisites

- Python 3.9+
- API keys for Google Generative AI and OpenAI

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application

```
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

### API Endpoints

- `POST /process-claim`: Process multiple PDF documents for an insurance claim
- `GET /health`: Health check endpoint

## Testing

Run the test suite with:

```
pytest
```
