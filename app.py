import streamlit as st
from agent.graph import build_graph
from agent.llm import add_to_memory

st.set_page_config(page_title="Grievance Assistant", layout="centered")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
if "state" not in st.session_state:
    st.session_state.state = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "step" not in st.session_state:
    st.session_state.step = "initial"
if "field_index" not in st.session_state:
    st.session_state.field_index = 0
if "current_missing" not in st.session_state:
    st.session_state.current_missing = []

st.title("📮 Grievance Assistant")

# Display previous chat messages
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

if st.session_state.step == "initial":
    prompt_question = "How can I assist you today? Please describe your grievance or query."

    # Only add to history once
    if not any(m["role"] == "assistant" and m["content"] == prompt_question for m in st.session_state.history):
        st.session_state.history.append({"role": "assistant", "content": prompt_question})

    # Display entire history
    for msg in st.session_state.history:
        st.chat_message(msg["role"]).write(msg["content"])
        
    user_input = st.chat_input("Describe your query")
    if user_input:
        add_to_memory("user", user_input)
        st.session_state.history.append({"role": "user", "content": user_input})
        state = {"prompt": user_input, "data": {}}
        result = st.session_state.graph.invoke(state)
        st.session_state.state = result
        st.session_state.current_missing = result.get("missing_fields", [])
        st.session_state.field_index = 0
        if st.session_state.current_missing:
            st.session_state.step = "collect_fields"
            st.rerun()
        else:
            st.session_state.step = "done"
            st.rerun()

elif st.session_state.step == "collect_fields":
    fields = st.session_state.current_missing
    idx = st.session_state.field_index
    data = st.session_state.state.get("data", {})

    if idx < len(fields):
        field = fields[idx]
        prompt_question = {
            "name": "What is your Name?",
            "mobile_number": "What is your Mobile Number?",
            "complaint_text": "Please describe your complaint.",
            "complaint_id": "Please enter your Complaint ID."
        }.get(field, f"Please provide {field.replace('_', ' ')}.")  # Add more as needed

        st.chat_message("assistant").write(prompt_question)
        user_field = st.chat_input("Your answer")

        if user_field is not None:
            user_field = user_field.strip()

            # Validation
            error = None
            if not user_field:
                error = "This field cannot be empty. Please enter a valid response."
            elif field == "mobile_number":
                if not (user_field.isdigit() and len(user_field) == 10):
                    error = "Please enter a valid 10-digit mobile number."

            if error:
                st.chat_message("assistant").error(error)
            else:
                st.session_state.history.append({"role": "assistant", "content": prompt_question})
                st.session_state.history.append({"role": "user", "content": user_field})
                data[field] = user_field
                add_to_memory("user", f"{field}: {user_field}")
                st.session_state.state["data"] = data
                st.session_state.field_index += 1
                if st.session_state.field_index < len(fields):
                    st.rerun()
                else:
                    # All fields collected, go to done
                    state = st.session_state.state
                    state["prompt"] = ""
                    result = st.session_state.graph.invoke(state)
                    st.session_state.state = result
                    st.session_state.step = "done"
                    st.rerun()
    else:
        st.session_state.step = "done"
        st.rerun()

elif st.session_state.step == "done":
    result = st.session_state.state.get("result", "Something went wrong.")
    st.session_state.history.append({"role": "assistant", "content": result})
    st.chat_message("assistant").success(result)
    if st.button("Do you need more help?"):
        st.session_state.clear()
        st.rerun()
