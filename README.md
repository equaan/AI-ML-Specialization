# MediAgent

MediAgent is a multimodal clinical decision support system built as an AI/ML specialization portfolio project. The current repository contains Phase 0 scaffolding, backend foundations, and setup documentation so development can continue smoothly on a higher-spec machine for model pulls and dataset ingestion.

## Current Status

- Project structure scaffolded
- FastAPI backend skeleton added
- ChromaDB setup utility added
- Core Pydantic schemas added
- Progress tracker and stronger-PC setup steps documented in `progress.md`

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_chromadb.py
uvicorn backend.main:app --reload
```

Then open:

- API health: `http://localhost:8000/api/health`
- API docs: `http://localhost:8000/docs`

## Next Steps

- Install Ollama on the stronger machine
- Pull `llama3.1:8b` and `llava:13b`
- Download datasets into `data/raw/`
- Build Phase 1 agents and ingestion scripts

See `TODO.md` for the task roadmap and `progress.md` for the handoff checklist.
