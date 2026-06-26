# AI Customer Support Assistant

## Overview
An AI-powered Customer Support Assistant built using RAG (Retrieval-Augmented Generation), FAISS, and Groq.

## Features
- PDF Upload
- FAQ Support
- AI Chat
- RAG-based Retrieval
- FAISS Vector Search
- Groq LLM Integration

## Tech Stack
- Python
- Streamlit
- FAISS
- LangChain
- Groq
- Sentence Transformers

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run rag.py
```

## Environment Variable

Create a `.env` file and add:

```text
GROQ_API_KEY=your_groq_api_key_here
```

## Project Structure

- config/
- data/
- faiss_index/
- utils/
- rag.py
- requirements.txt

## Author

Rajasri Ravipati
