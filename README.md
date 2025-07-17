# 🧠 RAG-Chatbot for Grievance Handling

A Retrieval-Augmented Generation (RAG) based chatbot that enables users to:

- 📄 Ask policy/SOP-based questions from internal documents.
- 📝 Create new grievance complaints via API.
- 🔍 Check the status of an existing complaint.

Built using **LangGraph**, **LanceDB**, **FastAPI**, and **Streamlit**.

---

## 🚀 Features

- Embeds and stores PDF documents for semantic search.
- Retrieves relevant document chunks to answer queries.
- Classifies user prompts into:
  - **Grievance Creation**
  - **Grievance Status Query**
  - **Policy/Document Q&A**
- Integrates with REST APIs to file or track grievances.

---

## 🛠 Setup Instructions

### 1. 🔑 Configure Groq API Key

Generate your [Groq API Key](https://console.groq.com/keys) and save it in a config file.
