import pytest
from fastapi.testclient import TestClient
import os
import io
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# This test would require sample PDF files
# def test_process_claim():
#     """Test the claim processing endpoint with sample PDFs."""
#     # Define test files
#     test_files = [
#         ("sample_bill.pdf", "application/pdf"),
#         ("sample_discharge.pdf", "application/pdf"),
#         ("sample_id_card.pdf", "application/pdf")
#     ]
#     
#     # Create file objects
#     files = []
#     for filename, content_type in test_files:
#         file_path = os.path.join("tests", "test_files", filename)
#         with open(file_path, "rb") as f:
#             file_content = f.read()
#         files.append(("files", (filename, file_content, content_type)))
#     
#     # Send request
#     response = client.post("/process-claim", files=files)
#     assert response.status_code == 200
#     
#     # Check response structure
#     result = response.json()
#     assert "documents" in result
#     assert "validation" in result
#     assert "claim_decision" in result