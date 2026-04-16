# MediAgent

MediAgent is a multimodal clinical decision support system built for an AI/ML specialization portfolio project.

It combines:

- Vision analysis for medical images
- RAG over medical knowledge sources
- Structured clinical report generation

## Architecture

Input modalities:

- Image (optional)
- Lab report PDF (optional)
- Symptoms text (required)
- Voice note (optional)

Pipeline:

1. Vision Agent extracts image findings
2. RAG Agent retrieves supporting medical context
3. Report Agent synthesizes a structured clinical report

API layer:

- FastAPI
- LangGraph orchestrator
- ChromaDB vector store
- Ollama-hosted local models

## Quick Start (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_chromadb.py
uvicorn backend.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

- API health: http://localhost:8000/api/health
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Evaluation Results

The following Phase 5 benchmark runs were completed and saved in `data/processed/evaluation`.

| Component | Dataset | Setup | Metric | Result |
|---|---|---|---|---|
| Vision Agent | HAM10000 | sample_size=50 | medical-image detection accuracy | 1.00 |
| RAG Agent | bigbio/med_qa (train) | sample_size=100, selection=first_n | MRR@5 | 0.079 |
| Full Pipeline | MedMCQA (train) | sample_size=50, selection=first_n | Top-1 accuracy | 0.28 (14/50) |

Artifacts:

- Vision: `data/processed/evaluation/vision_ham10000_eval.json` and `data/processed/evaluation/vision_ham10000_eval.md`
- RAG: `data/processed/evaluation/rag_medqa_mrr_eval.json` and `data/processed/evaluation/rag_medqa_mrr_eval.md`
- Pipeline: `data/processed/evaluation/pipeline_medmcqa_accuracy_eval.json` and `data/processed/evaluation/pipeline_medmcqa_accuracy_eval.md`

## How It Works

- Endpoint `POST /api/analyze` accepts multipart input and runs the LangGraph workflow.
- Endpoint `POST /api/transcribe` runs Whisper for voice-to-text.
- Endpoint `GET /api/models/status` reports model and vector store availability.
- Endpoint `GET /api/export/{session_id}` returns report exports.

## Current Status

- Phases 0-4 completed
- Phase 5 evaluation tasks completed
- Remaining Phase 5 work includes README polish items (banner/demo assets), deployment, and portfolio presentation tasks

## Clinical Disclaimer

MediAgent is a clinical decision support prototype for educational and portfolio use.
It does not replace professional medical judgment, diagnosis, or treatment decisions.

## Project Tracking

- Task roadmap: `docs/TODO.md`
- Implementation log: `docs/progress.md`
- Product/design docs: `docs/`
