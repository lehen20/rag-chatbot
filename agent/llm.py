from groq import Groq
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage
import re
import os 
import yaml
import time

if not os.path.exists('config.yml'):
    raise FileNotFoundError()
    
with open('config.yml') as f:
    config = yaml.safe_load(f)

# client = Together(api_key=config['api_key'])
client = Groq(api_key=config['groq_api_key'])

memory = ConversationBufferMemory(return_messages=True)

def extract_complaint_id_from_memory():
    messages = memory.chat_memory.messages[::-1]  # Reverse: latest first

    for msg in messages:
        if isinstance(msg, AIMessage):
            # Match UUID pattern
            match = re.search(r"complaint ID is\s+([a-f0-9\-]{36})", msg.content, re.IGNORECASE)
            if match:
                return match.group(1)
    return None

def add_to_memory(role, content):
    if role == "user":
        memory.chat_memory.add_user_message(content)
    else:
        memory.chat_memory.add_ai_message(content)

def get_memory_messages():
    return memory.chat_memory.messages

def classify_intent_with_memory(prompt: str) -> str:
    memory.chat_memory.add_user_message(prompt)

    full_context = [
        {"role": "system", "content": "Classify the user's intent as one of the following: complaint_create, status_check, or other. Respond ONLY with the label."}
    ]

    for msg in get_memory_messages()[-5:]:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        full_context.append({"role": role, "content": msg.content})
        
    start_time = time.time()
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=full_context,
        temperature=0,
        max_completion_tokens=10,
        top_p=0,
        stream=False,
        stop=None,
    )
    label = response.choices[0].message.content.strip().lower()
    print(f"{label=}")
    memory.chat_memory.add_ai_message(label)
    print(f'{time.time() - start_time=}')
    return label

# IN CASE NEED TO USE TOGETHER INSTEAD OF GROQ
# from together import Together
# def classify_intent_with_memory(prompt: str) -> str:
#     memory.chat_memory.add_user_message(prompt)

#     full_context = [
#         {"role": "system", "content": "Classify the user's intent as one of the following: complaint_create, status_check, or other. Respond ONLY with the label."}
#     ]

#     for msg in get_memory_messages()[-5:]:  # Use recent messages only for brevity
#         role = "assistant" if isinstance(msg, AIMessage) else "user"
#         full_context.append({"role": role, "content": msg.content})
    
#     print(f"{full_context=}")
#     start_time = time.time()
#     print(f'{start_time=}')
#     response = client.chat.completions.create(
#         model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#         messages=full_context,
#         stream=False
#     )
#     label = response.choices[0].message.content.strip().lower()
#     print(f"{label=}")
#     memory.chat_memory.add_ai_message(label)
#     print(f'{time.time() - start_time=}')
#     return label
