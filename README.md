## AURA AI Agronomist

### Tech Stack
- FastAPI
- Groq LLM (LLaMA 3.3 70B)
- ChromaDB + Sentence Transformers
- HTML/CSS/JS frontend

### How it Works
The chatbot uses two intelligence levels:
1. Level-1 uses RAG to answer farming questions from a knowledge base.
2. Level-2 analyzes real farm sensor data to diagnose exact crop issues.

### Setup
```bash
cd backend
pip install -r requirements.txt
python setup_rag.py
uvicorn main:app --reload
