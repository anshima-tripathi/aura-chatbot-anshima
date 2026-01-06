# 🌱 AURA AI Agronomist

An intelligent, sensor-aware AI agronomy assistant that combines  
**RAG (Retrieval-Augmented Generation)**, **Rule-Based Diagnosis**, and **LLMs**  
to deliver **accurate, explainable, and data-backed crop insights**.

> ⚠️ This is NOT a generic chatbot.  
> This is a **decision-aware AI system** designed for real farms.

---

## 🚀 Key Capabilities

- 🌾 Crop-specific knowledge (Lettuce supported)
- 🧠 Retrieval-Augmented Generation (RAG) using ChromaDB
- 📡 Sensor-aware diagnosis (EC, Temperature, pH, Light)
- 📊 Rule-based agronomy engine (no hallucinations)
- 🤖 Groq LLM integration (LLaMA 3.3 – 70B)
- ⚡ FastAPI backend + clean frontend UI

---

## 🧠 System Architecture (High-Level)

```mermaid
flowchart TD
    U[User Question] --> UI[Chat UI]

    UI --> L1[Level 1<br/>Knowledge-Based AI]
    UI --> L2[Level 2<br/>Sensor-Aware AI]

    %% LEVEL 1
    L1 --> RAG[Vector Retriever<br/>(ChromaDB)]
    RAG --> KB[Agricultural Knowledge Base]
    RAG --> LLM1[Groq LLM]
    LLM1 --> A1[Context-Aware Answer]

    %% LEVEL 2
    L2 --> SYM[LLM Symptom Detection<br/>(Classification Only)]
    L2 --> SENS[Farm Sensor Data<br/>(EC, Temp, pH, Light)]
    SYM --> RULES[Rule-Based Diagnostic Engine]
    SENS --> RULES
    RULES --> A2[Final Diagnosis<br/>(Cause + Action)]
