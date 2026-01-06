import chromadb
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

client = chromadb.Client()
collection = client.get_or_create_collection("agri_knowledge")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_knowledge():
    with open(DATA_DIR / "agricultural_knowledge_base.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    metadatas = []
    ids = []

    i = 0
    for crop, details in data.items():
        for key, value in details.items():
            docs.append(f"{crop} - {key}: {value}")
            metadatas.append({"crop": crop})
            ids.append(str(i))
            i += 1

    embeddings = embedder.encode(docs).tolist()
    collection.add(documents=docs, embeddings=embeddings, metadatas=metadatas, ids=ids)

def retrieve_context(query: str, k: int = 3) -> str:
    embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return "\n".join(results["documents"][0])
