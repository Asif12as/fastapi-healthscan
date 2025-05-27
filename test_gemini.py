import asyncio
import sys
from app.utils.llm_utils import classify_document_with_gemini

async def test_gemini():
    try:
        result = await classify_document_with_gemini('This is a hospital bill for $500', 'hospital_bill.pdf')
        print(f'Classification result: {result}')
    except Exception as e:
        print(f'Error occurred: {str(e)}')

if __name__ == "__main__":
    asyncio.run(test_gemini())