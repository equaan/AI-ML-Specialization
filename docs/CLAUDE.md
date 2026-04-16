# CLAUDE.md — MediAgent Project Intelligence

## Project Identity

**Project Name:** MediAgent — Multimodal Clinical Decision Support Agent  
**Type:** AI/ML Specialization Portfolio Project (3rd Year — Vidyalankar Institute of Technology)  
**Domain:** Healthcare / Medical AI  
**Stack:** Python · LangGraph · LangChain · FastAPI · ChromaDB · LLaVA · BioBERT · Whisper · React  
**Goal:** A multimodal, multi-agent clinical decision support system that takes patient images, lab reports (PDFs), and symptom descriptions (text/voice) and returns structured differential diagnoses with confidence scores and red-flag alerts.

---

## Architecture Overview

```
User Input (Image + PDF + Text/Voice)
        │
        ▼
  FastAPI Gateway
        │
        ▼
  LangGraph Orchestrator  ◄──────────────────────────────────┐
        │                                                      │
   ┌────┴──────────────────────────────────────┐              │
   │              Agent Pipeline               │              │
   │                                           │              │
   │  ┌──────────────┐  ┌──────────────────┐  │              │
   │  │ Vision Agent │  │   RAG Agent      │  │              │
   │  │ (LLaVA /     │  │ (BioBERT +       │  │              │
   │  │  BioViL-T)   │  │  ChromaDB +      │  │              │
   │  │              │  │  PubMed/MedQA)   │  │              │
   │  └──────┬───────┘  └──────┬───────────┘  │              │
   │         │                 │               │              │
   │         └────────┬────────┘               │              │
   │                  │                        │              │
   │         ┌────────▼─────────┐             │              │
   │         │  Report Agent    │             │              │
   │         │ (Clinical        │             │              │
   │         │  Summarizer)     │             │              │
   │         └────────┬─────────┘             │              │
   └──────────────────┼────────────────────────┘              │
                      │                                        │
                      ▼                                        │
              Structured Output ───────────────────────────────┘
              (JSON + Markdown)
                      │
                      ▼
              React Frontend (Google Stitch)
```

---

## Repository Structure

```
mediagent/
├── README.md               ← Repo face/introduction
├── docs/
│   ├── CLAUDE.md           ← This file
│   ├── PRD.md              ← Product Requirements Document
│   ├── TODO.md             ← Phased task tracker
│   ├── PROMPTS.md          ← LLM prompt templates
│   ├── STITCH.md           ← Google Stitch frontend prompt
│   ├── DATASETS.md         ← Dataset guide
│   └── progress.md         ← Build/run history
│
├── backend/
│   ├── main.py             ← FastAPI entry point
│   ├── config.py           ← Env vars, model paths, settings
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py ← LangGraph state machine
│   │   ├── vision_agent.py ← Image analysis (LLaVA)
│   │   ├── rag_agent.py    ← Medical knowledge retrieval
│   │   └── report_agent.py ← Final clinical summary
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py   ← Lab report PDF extraction
│   │   ├── voice_input.py  ← Whisper transcription
│   │   ├── pubmed_tool.py  ← PubMed API tool
│   │   └── image_loader.py ← Image preprocessing
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embedder.py     ← BioBERT embeddings
│   │   ├── vectorstore.py  ← ChromaDB CRUD
│   │   └── ingest.py       ← Dataset ingestion scripts
│   ├── models/
│   │   └── schemas.py      ← Pydantic models
│   └── utils/
│       ├── logger.py
│       └── helpers.py
│
├── frontend/               ← React app (Google Stitch generated)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
│
├── data/
│   ├── raw/                ← Raw datasets (gitignored)
│   └── processed/          ← Chunked + embedded docs
│
├── scripts/
│   ├── ingest_pubmed.py
│   ├── ingest_medqa.py
│   └── setup_chromadb.py
│
├── tests/
│   ├── test_vision_agent.py
│   ├── test_rag_agent.py
│   └── test_api.py
│
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Tech Stack & Model Choices

| Layer | Technology | Why |
|---|---|---|
| Orchestration | LangGraph | Stateful multi-agent graph, perfect for sequential + parallel agent flows |
| LLM Backend | LLaMA 3.1 8B via Ollama | Fully open source, runs locally, no API cost |
| Vision Model | LLaVA 1.6 (13B) or BioViL-T | Multimodal image+text understanding |
| Embeddings | BioBERT / PubMedBERT | Domain-specific medical embeddings |
| Vector Store | ChromaDB | Lightweight, local, open source |
| PDF Parsing | PyMuPDF (fitz) | Fast, accurate text+table extraction |
| Voice | OpenAI Whisper (local) | Open source speech-to-text |
| API Layer | FastAPI | Async, fast, type-safe |
| Frontend | React + Tailwind (Stitch) | Clean SPA, component-driven |
| Tracing | LangSmith | Agent trace visualization |
| Containerization | Docker + Docker Compose | Reproducible dev environment |

---

## Agent Definitions

### 1. Vision Agent (`vision_agent.py`)
- **Input:** Medical image (X-ray, skin lesion, eye fundus, etc.)
- **Model:** LLaVA 1.6 via Ollama
- **Output:** Structured JSON with `{findings: [], anomalies: [], image_type: "", confidence: float}`
- **Prompt:** See `docs/PROMPTS.md → VISION_AGENT_PROMPT`

### 2. RAG Agent (`rag_agent.py`)
- **Input:** Patient symptoms (text) + Vision Agent findings
- **Tools:** ChromaDB retriever, PubMed API search tool
- **Knowledge Base:** MedQA chunks + PubMed abstracts (ingested at setup)
- **Output:** `{relevant_conditions: [], supporting_evidence: [], sources: []}`
- **Prompt:** See `docs/PROMPTS.md → RAG_AGENT_PROMPT`

### 3. Report Agent (`report_agent.py`)
- **Input:** Outputs from Vision Agent + RAG Agent
- **Model:** LLaMA 3.1 8B via Ollama
- **Output:** Final structured clinical report JSON
- **Schema:**
```json
{
  "patient_summary": "...",
  "differential_diagnosis": [
    {"condition": "...", "confidence": 0.85, "icd_code": "..."},
  ],
  "red_flags": ["..."],
  "recommended_next_steps": ["..."],
  "disclaimer": "For clinical review only. Not a substitute for professional diagnosis."
}
```
- **Prompt:** See `docs/PROMPTS.md → REPORT_AGENT_PROMPT`

---

## LangGraph State Schema

```python
from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class MediAgentState(TypedDict):
    # Inputs
    patient_symptoms: str
    image_path: Optional[str]
    pdf_path: Optional[str]
    voice_transcript: Optional[str]

    # Agent outputs
    vision_findings: Optional[dict]
    rag_context: Optional[dict]
    final_report: Optional[dict]

    # Metadata
    messages: List[BaseMessage]
    current_agent: str
    error: Optional[str]
```

---

## Environment Variables

```env
# .env.example
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
VISION_MODEL=llava:13b
CHROMADB_PATH=./data/chromadb
PUBMED_API_KEY=your_pubmed_api_key
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=mediagent
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

---

## Key Development Rules

1. **All models run locally via Ollama** — no OpenAI calls in production code.
2. **Every agent returns a typed Pydantic schema** — no raw string outputs.
3. **LangGraph state is immutable** — agents return updated state dicts, never mutate.
4. **FastAPI endpoints are async** — use `async def` everywhere.
5. **Medical disclaimer is mandatory** on every report output.
6. **No patient data is persisted** — all uploads are temp files, deleted after processing.
7. **Whisper runs locally** — `whisper.load_model("base")` unless GPU available.
8. **ChromaDB collections:**
   - `medqa_chunks` — MedQA dataset embeddings
   - `pubmed_abstracts` — PubMed abstract embeddings
   - `medical_guidelines` — WHO/CDC guidelines

---

## Datasets & Knowledge Sources (All Open Source)

| Dataset | Source | Use |
|---|---|---|
| MedQA (USMLE) | HuggingFace `bigbio/med_qa` | RAG knowledge base |
| PubMed Abstracts | NCBI E-utilities API | Live tool retrieval |
| MedMCQA | HuggingFace `medmcqa` | Evaluation |
| MIMIC-CXR (if available) | PhysioNet | X-ray vision eval |
| Skin HAM10000 | Kaggle / HuggingFace | Skin lesion testing |

---

## Running the Project

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/mediagent
cd mediagent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Pull models via Ollama
ollama pull llama3.1:8b
ollama pull llava:13b

# 3. Ingest knowledge base
python scripts/ingest_medqa.py
python scripts/ingest_pubmed.py

# 4. Start backend
uvicorn backend.main:app --reload --port 8000

# 5. Start frontend (separate terminal)
cd frontend && npm install && npm run dev
```

---

## Common Pitfalls to Avoid

- **LLaVA hallucinations on non-medical images** — always validate `image_type` before proceeding.
- **ChromaDB cold start** — run ingestion scripts before first query.
- **Ollama RAM usage** — LLaVA 13B needs ~16GB RAM; use `llava:7b` for lower spec machines.
- **PDF parsing edge cases** — scanned PDFs won't parse with PyMuPDF; add OCR fallback with `pytesseract`.
- **LangGraph cycles** — avoid unconditional loops; always add termination conditions.

---

## Evaluation Metrics

| Agent | Metric | Target |
|---|---|---|
| Vision Agent | Precision on image classification | > 75% |
| RAG Agent | Retrieval MRR@5 on MedQA | > 0.65 |
| Full Pipeline | End-to-end answer accuracy on MedMCQA | > 60% |
| Latency | Total pipeline response time | < 30s |

---

## Resume-Worthy Talking Points

- "Designed a stateful 3-agent LangGraph pipeline with parallel vision and RAG sub-graphs"
- "Built domain-specific RAG over 200K+ PubMed abstracts using PubMedBERT embeddings"
- "Integrated LLaVA 1.6 for multimodal medical image analysis within an agentic workflow"
- "Achieved end-to-end inference with zero external API calls using Ollama local inference"
- "Implemented structured clinical output schema with ICD-10 code mapping and confidence scoring"
