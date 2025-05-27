from typing import Dict, Any, List
from ..agents.bill_agent import BillAgent
from ..agents.discharge_agent import DischargeAgent
from ..agents.id_card_agent import IdCardAgent
from ..agents.base_agent import BaseAgent

# Agent factory
def get_agent_for_document_type(doc_type: str) -> BaseAgent:
    """Return the appropriate agent for a document type."""
    agents = {
        "bill": BillAgent(),
        "discharge_summary": DischargeAgent(),
        "id_card": IdCardAgent()
    }
    return agents.get(doc_type, None)

async def extract_structured_data(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process each document with the appropriate agent to extract structured data.
    """
    results = []
    
    for doc in documents:
        agent = get_agent_for_document_type(doc["type"])
        
        if agent:
            # Process document with the appropriate agent
            structured_data = await agent.process(doc["content"])
            
            # Add validation issues
            validation_issues = agent.validate(structured_data)
            structured_data["validation_issues"] = validation_issues
            
            results.append(structured_data)
    
    return results