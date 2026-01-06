from groq import Groq
import os
from llm.rag_engine import retrieve_context

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(question: str) -> str:
    context = retrieve_context(question)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI agronomist. Answer strictly using the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
