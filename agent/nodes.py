from agent.llm import classify_intent_with_memory, add_to_memory, extract_complaint_id_from_memory, call_llm_with_prompt
from agent.call_api import register_complaint, get_complaint_status
from rag.retrieve_documents import retrieve_similar_chunks
from pydantic import ValidationError

def input_node(state):
    return state

def classify_node(state):
    user_prompt = state["prompt"]
    intent = classify_intent_with_memory(user_prompt)
    print(f"{intent=}")
    return {"intent": intent}

def gather_node(state):
    intent = state["intent"]
    data = state.get("data", {})

    required_fields = {
        "complaint_create": ["name", "mobile_number", "complaint_text"],
        "status_check": ["complaint_id"],
        "policy_question": [],
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
    user_prompt = state["prompt"]
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
        elif intent == "policy_question":
            # --- Vector Search Step ---
            context_chunks = retrieve_similar_chunks(user_prompt, top_k=5)  # List of text chunks
            
            # Combine into a single context
            context_text = "\n\n".join(context_chunks)

            # --- LLM Prompt Step ---
            final_prompt = f"Answer the following using context:\n{context_text}\n\nQuestion: {user_prompt}"
            answer = call_llm_with_prompt(context_text, user_prompt)

            return {"result": answer, "raw": {"prompt": final_prompt, "context": context_chunks}}
        else:
            return {"result": "Unsupported intent", "raw": None}
    except (ValidationError, ValueError) as e:
        return {"result": f"Validation error: {str(e)}", "raw": None}


