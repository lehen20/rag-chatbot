# RAG-Chatbot for Grievance Handling

A Retrieval-Augmented Generation (RAG) based chatbot that enables users to:

- Create new grievance complaints via API.
- Check the status of an existing complaint.
- **ADDITIONAL FEATURE: Ask policy/SOP-based questions from internal documents.**

Built using **LangGraph**, **LanceDB**, **FastAPI**, and **Streamlit**.

---

## Features

- Classifies user prompts into:
  - **Grievance Creation**
  - **Grievance Status Query**
  - **Policy/Document Q&A**
- Integrates with REST APIs to file or track grievances.
- Embeds and stores PDF documents for semantic search.
- Retrieves relevant document chunks to answer queries.

---
## Anaconda and Requirements

Install dependencies
```bash
conda create -n chatbot python=3.10
conda activate chatbot
pip install -r requirements.txt
```

---

## Setup Instructions

### 1. Configure Groq API Key

Generate your [Groq API Key](https://console.groq.com/keys) and save it in a config file.
Create a `.yml` file at the project root:

```bash
groq_api_key=your_groq_api_key_here
```

### 2. One time document ingestion

Ingest PDFs and store their embeddings in LanceDB:
```bash
cd rag
python ingest_documents.py
```
This will:

- Read all PDFs in rag/documents/

- Embed paragraphs using all-MiniLM-L6-v2

- Store them in rag/lancedb_data as a LanceDB table

### 3. Start FastAPI Backend

```bash
cd backend
uvicorn main:app --port 8000
```

### 4. Launch the chat interface 

```bash
streamlit run app.py
```