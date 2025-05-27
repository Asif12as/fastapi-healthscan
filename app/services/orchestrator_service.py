from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import asyncio

from ..services.document_service import process_documents
from ..services.ai_service import extract_structured_data
from ..services.validation_service import validate_claim_documents
from ..models.schemas import ClaimProcessingResult

class ClaimProcessingState(Dict):
    """State object for the claim processing workflow."""
    files: List[Any]
    processed_documents: List[Dict[str, Any]] = None
    structured_data: List[Dict[str, Any]] = None
    validation_result: Dict[str, Any] = None
    claim_decision: Dict[str, Any] = None
    final_result: Dict[str, Any] = None

async def document_processor(state: ClaimProcessingState) -> ClaimProcessingState:
    """Process the uploaded documents to extract text and classify them."""
    processed_documents = await process_documents(state["files"])
    return {"processed_documents": processed_documents}

async def data_extractor(state: ClaimProcessingState) -> ClaimProcessingState:
    """Extract structured data from the processed documents."""
    structured_data = await extract_structured_data(state["processed_documents"])
    return {"structured_data": structured_data}

async def claim_validator(state: ClaimProcessingState) -> ClaimProcessingState:
    """Validate the claim based on the structured data."""
    validation_result, claim_decision = validate_claim_documents(state["structured_data"])
    return {
        "validation_result": validation_result.model_dump(),
        "claim_decision": claim_decision.model_dump()
    }

async def result_formatter(state: ClaimProcessingState) -> ClaimProcessingState:
    """Format the final result."""
    documents = state["structured_data"]
    # Remove internal fields like validation_issues
    for doc in documents:
        if "validation_issues" in doc:
            del doc["validation_issues"]
    
    final_result = {
        "documents": documents,
        "validation": state["validation_result"],
        "claim_decision": state["claim_decision"]
    }
    return {"final_result": final_result}

def create_workflow_graph():
    """Create and configure the workflow graph for claim processing."""
    # Create a new graph
    graph = StateGraph(ClaimProcessingState)
    
    # Add nodes
    graph.add_node("document_processor", document_processor)
    graph.add_node("data_extractor", data_extractor)
    graph.add_node("claim_validator", claim_validator)
    graph.add_node("result_formatter", result_formatter)
    
    # Define the workflow
    graph.add_edge("document_processor", "data_extractor")
    graph.add_edge("data_extractor", "claim_validator")
    graph.add_edge("claim_validator", "result_formatter")
    graph.add_edge("result_formatter", END)
    
    # Set the entrypoint
    graph.set_entry_point("document_processor")
    
    return graph.compile()

async def process_claim(files: List[Any]) -> ClaimProcessingResult:
    """Process a claim using the workflow graph."""
    graph = create_workflow_graph()
    initial_state = {"files": files}
    
    # Run the workflow
    result = await graph.ainvoke(initial_state)
    
    return result["final_result"]