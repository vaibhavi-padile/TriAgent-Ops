from langgraph.graph import StateGraph, END
from state import AuditState
from agents import OperationsAgents

# Initialize the workflow graph
workflow = StateGraph(AuditState)
agents = OperationsAgents()

# Define graph nodes
workflow.add_node("Extractor", agents.extractor_agent)
workflow.add_node("Validator", agents.validator_agent)
workflow.add_node("Reporter", agents.reporter_agent)

# Set up graph transitions
workflow.set_entry_point("Extractor")
workflow.add_edge("Extractor", "Validator")

# Define conditional routing logic based on Validator's assessment
def route_after_validation(state: AuditState):
    if state["requires_human_review"]:
        print("🙋‍♂️ [Routing] Redirecting to Human-In-The-Loop Interface.")
        return "Reporter" # Let reporter generate the flagged brief for the human
        
    if state["validation_errors"] and state["validation_attempts"] < 2:
        print(f"🔄 [Routing] Validation failed. Looping back to Extractor (Attempt {state['validation_attempts']}).")
        return "Extractor"
        
    print("🚀 [Routing] Validation passed or maximum attempts hit. Moving to Reporter.")
    return "Reporter"

workflow.add_conditional_edges(
    "Validator",
    route_after_validation,
    {
        "Extractor": "Extractor",
        "Reporter": "Reporter"
    }
)

workflow.add_edge("Reporter", END)

# Compile graph into an executable application
app = workflow.compile()

# ---- Test Execution Setup ----
if __name__ == "__main__":
    # Create a mock unstructured document file to test
    mock_doc = "sample_contract.txt"
    with open(mock_doc, "w") as f:
        f.write("Agreement details: This contract is executed by Unknown Startup Ltd for an amount of -$5000. Payment terms are Net 90.")

    initial_state = {
        "raw_document_path": mock_doc,
        "extracted_data": None,
        "validation_errors": [],
        "validation_attempts": 0,
        "requires_human_review": False,
        "confidence_score": 1.0,
        "final_report_path": None
    }

    print("🏁 Starting Multi-Agent Operational Pipeline...")
    final_output = app.invoke(initial_state)
    print(f"\n🎯 Processing Complete! Output saved to: {final_output['final_report_path']}")
