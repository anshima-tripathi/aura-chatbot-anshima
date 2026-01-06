from dotenv import load_dotenv
import os
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 🔹 Load environment variables
load_dotenv()
print("GROQ KEY LOADED:", os.getenv("GROQ_API_KEY") is not None)

# 🔹 Import Groq LLM
from llm.groq_client import ask_llm

# 🔹 FastAPI app
app = FastAPI(
    title="AURA AI Agronomist",
    version="1.0.0"
)

# 🔹 CORS (frontend support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ---------- LOAD DATA ----------
with open(DATA_DIR / "sample_farm_data.json", "r", encoding="utf-8") as f:
    farm_json = json.load(f)

with open(DATA_DIR / "diagnostic_rules.json", "r", encoding="utf-8") as f:
    DIAGNOSTIC_RULES = json.load(f)

with open(DATA_DIR / "agricultural_knowledge_base.json", "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = json.load(f)

FARMS = farm_json["farms"]
OPTIMAL_RANGES = farm_json["optimal_ranges"]
ISSUE_IMPACT = farm_json["issue_impact_descriptions"]

FARM_INDEX = {farm["farmId"]: farm for farm in FARMS}

# ---------- MODELS ----------
class ChatRequest(BaseModel):
    message: str

# ---------- ROUTES ----------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AURA backend running",
        "farms_loaded": list(FARM_INDEX.keys())
    }

@app.get("/api/farms/{farm_id}/sensors")
def get_farm_sensors(farm_id: str):
    farm = FARM_INDEX.get(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm["sensors"]

@app.get("/api/farms/{farm_id}/history")
def get_farm_history(farm_id: str):
    farm = FARM_INDEX.get(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@app.get("/api/knowledge/{crop}")
def get_crop_knowledge(crop: str):
    data = KNOWLEDGE_BASE.get(crop)
    if not data:
        raise HTTPException(status_code=404, detail="Crop knowledge not found")
    return data

@app.post("/api/diagnose/{farm_id}")
def diagnose_farm(farm_id: str):
    farm = FARM_INDEX.get(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    if not farm.get("hasIssue"):
        return {"status": "healthy", "message": "No issues detected"}

    issue = farm.get("issueType")
    return {
        "issue": issue,
        "impact": ISSUE_IMPACT.get(issue, {}),
        "recommendation": DIAGNOSTIC_RULES.get(issue, {
            "summary": "No rule-based recommendation available"
        })
    }

# ---------- 🔥 REAL AI CHAT (Groq LLM) ----------

@app.post("/api/chat")
def chat_with_agronomist(req: ChatRequest, farm_id: str | None = None):
    # LEVEL 2 → sensor connected
    if farm_id:
        farm = FARM_INDEX.get(farm_id)
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        sensors = farm["sensors"]
        issues = []

        # Rule 1: EC
        if sensors["ec"] < 1.2:
            issues.append(
                f"EC is low ({sensors['ec']}), causing nutrient deficiency."
            )

        # Rule 2: Temperature
        if sensors["temperature"] < 18:
            issues.append(
                f"Temperature is low ({sensors['temperature']}°C), causing cold stress."
            )

        # Rule 3: Light
        if sensors["ppfd"] < 200:
            issues.append(
                f"Light intensity is low ({sensors['ppfd']} PPFD)."
            )

        if issues:
            return {
                "reply": "I checked your farm sensors:\n" + "\n".join(issues),
                "source": "Sensor Diagnosis"
            }
        else:
            return {
                "reply": "All sensor parameters look optimal.",
                "source": "Sensor Diagnosis"
            }

    # LEVEL 1 → RAG
    reply = ask_llm(req.message)
    return {
        "reply": reply,
        "source": "Groq LLM + RAG"
    }
