from langgraph.graph import StateGraph
from typing import TypedDict, Optional, Dict, Any

from agent.nodes import input_node, classify_node, gather_node, validate_and_call_api_node

class AgentState(TypedDict):
    prompt: str
    intent: Optional[str]
    data: Dict[str, Any]
    missing_fields: Optional[list]
    result: Optional[str]

# STATE = {"prompt": str, "intent": str, "data": dict, "result": str}

def build_graph():
    builder = StateGraph(state_schema=AgentState)

    builder.add_node("input", input_node)
    builder.add_node("classify_intent", classify_node)
    builder.add_node("gather_info", gather_node)
    builder.add_node("validate_and_call_api", validate_and_call_api_node)
    builder.add_node("end", lambda x: x)

    builder.set_entry_point("input")

    builder.add_edge("input", "classify_intent")
    builder.add_edge("classify_intent", "gather_info")
    builder.add_edge("gather_info", "validate_and_call_api")
    builder.add_edge("validate_and_call_api", "end")

    builder.set_finish_point("end")
    return builder.compile()
