from agent.llm import classify_intent_with_memory, add_to_memory, extract_complaint_id_from_memory
from agent.call_api import register_complaint, get_complaint_status
from pydantic import ValidationError

def input_node(state):
    return state

def classify_node(state):
    user_prompt = state["prompt"]
    intent = classify_intent_with_memory(user_prompt)
    return {"intent": intent}

def gather_node(state):
    intent = state["intent"]
    data = state.get("data", {})

    required_fields = {
        "complaint_create": ["name", "mobile_number", "complaint_text"],
        "status_check": ["complaint_id"]
    }

    if intent not in required_fields:
        return {"missing_fields": [], "data": data}

    # complaint_id from memory
    if intent == "status_check" and not data.get("complaint_id"):
        complaint_id_from_memory = extract_complaint_id_from_memory()
        if complaint_id_from_memory:
            data["complaint_id"] = complaint_id_from_memory

    missing = [f for f in required_fields[intent] if not data.get(f)]
    return {"missing_fields": missing, "data": data}

def validate_and_call_api_node(state):
    intent = state["intent"]
    data = state["data"]
    try:
        if intent == "complaint_create":
            response = register_complaint(data)
            complaint_id = response.get("complaint_id")
            if complaint_id:
                add_to_memory("assistant", f"Your complaint ID is {complaint_id}")
            
            result_msg = f"Your complaint has been registered successfully. Your complaint ID is {complaint_id}."
            return {"result": result_msg, "raw": response}
        elif intent == "status_check":
            if not data.get("complaint_id"):
                raise ValueError("Complaint ID is required for status check.")
            response = get_complaint_status(data)
            
            status = response.get("status", "Unknown")
            result_msg = (
                f"The status of your complaint (ID: {data['complaint_id']}) is: {status}."
            )
            return {"result": result_msg, "raw": response}
        else:
            return {"result": "Unsupported intent", "raw": None}
    except (ValidationError, ValueError) as e:
        return {"result": f"Validation error: {str(e)}", "raw": None}


