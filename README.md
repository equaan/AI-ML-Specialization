# MediAgent

MediAgent is a multimodal clinical decision support prototype built as an AI/ML specialization portfolio project.

It combines four input channels (symptoms text, image, PDF lab report, voice note) and produces a structured clinical report with differential diagnosis, risk flags, and evidence-backed next steps.

## 1) What This Project Does

MediAgent is designed to support (not replace) clinical reasoning by:

- interpreting medical images through a vision model
- parsing and summarizing lab report PDFs
- transcribing voice notes into symptoms text
- retrieving supporting context from a local medical knowledge base (RAG)
- synthesizing outputs into a normalized report format for UI rendering and export

Primary output format includes:

- patient summary
- ranked differential diagnosis
- red flags
- recommended next steps
- clinical disclaimer

## 2) Current Runtime Status (Important)

### Are we currently using docker-compose?

Short answer: **not in the default workflow**.

What is active today:

- backend runs directly via Python/uvicorn
- frontend runs via Vite (Node)
- demo launcher uses `scripts/start_demo_stack.ps1`
- Ollama is started from local binary (`D:\Ollama\ollama.exe`) by the launcher script
- Chroma is used as a **local persistent store** via `chromadb.PersistentClient(path=...)`

What `docker-compose.yml` currently provides:

- an Ollama container
- a Chroma container

Why compose is not the main path right now:

- the launcher script does not call Docker Compose
- backend vector store integration uses local disk path (`CHROMADB_PATH`) instead of Chroma HTTP server mode

So, Compose is available as optional infrastructure scaffolding, but not the primary execution path in this repository version.

## 3) System Architecture

### High-level flow

1. User submits one or more inputs (text/image/pdf/voice)
2. API normalizes inputs
3. Voice notes are transcribed (if provided)
4. PDF lab report is parsed and summarized (if provided)
5. Orchestrator runs agent pipeline:
	- Vision Agent
	- RAG Agent
	- Report Agent
6. Final report is saved by session id
7. Frontend renders report and supports export

### Backend stack

- FastAPI service
- LangGraph-style orchestration (`backend/agents/orchestrator.py`)
- Ollama model provider (LLM + VLM)
- ChromaDB local persistent vector store
- PyMuPDF for PDF export

### Frontend stack

- React + Vite
- page-oriented UI with analysis, evidence, records, status, and trace views
- API proxy setup via Vite for same-origin local development

## 4) Repository Structure

Top-level layout:

- `backend/` API, agents, tools, RAG, models, utils
- `frontend/` React app
- `scripts/` ingestion, setup, evaluation, and demo startup scripts
- `tests/` backend and pipeline tests
- `docs/` planning, PRD, prompts, progress log, datasets guide
- `data/` sample inputs, local vector DB files, and evaluation artifacts

Key docs:

- `docs/README.md` documentation index
- `docs/TODO.md` phase checklist
- `docs/progress.md` implementation and benchmark log
- `docs/PRD.md` product requirements

## 5) API Endpoints

From `backend/main.py`:

- `GET /` basic service message
- `GET /api/health` core health (Ollama + Chroma)
- `GET /api/models/status` model availability status
- `POST /api/transcribe` voice to text
- `POST /api/analyze` multimodal analysis pipeline
- `GET /api/export/{session_id}?format=json|markdown|pdf` report export
- `GET /health` compatibility alias for demos/tunnel checks
- `GET /stats` compatibility quick status endpoint

## 6) Local Setup (Recommended Path)

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Ollama installed locally with required models pulled

### Backend setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_chromadb.py
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### Access points

- API docs: http://127.0.0.1:8000/docs
- API health: http://127.0.0.1:8000/api/health
- Frontend: http://127.0.0.1:3000

## 7) One-Command Demo Startup (Windows)

Use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_demo_stack.ps1
```

This script:

- kills stale local processes/ports
- starts Ollama, backend, frontend
- creates ngrok tunnel
- probes public `/health` and `/stats`
- writes tunnel URL to `ngrok_url.txt`

## 8) Optional Docker Compose

The repository includes `docker-compose.yml` for:

- `ollama` on `11434`
- `chromadb` on host port `8001`

You can start it with:

```bash
docker compose up -d
```

Notes:

- This is optional and not integrated into the default launcher.
- Current backend Chroma integration uses local persistent path storage, not Chroma HTTP API mode.

## 9) Data, Evaluation, and Benchmarks

Evaluation artifacts are stored under `data/processed/evaluation`.

Latest recorded metrics:

| Component | Dataset | Setup | Metric | Result |
|---|---|---|---|---|
| Vision Agent | HAM10000 | sample_size=50 | medical-image detection accuracy | 1.00 |
| RAG Agent | bigbio/med_qa (train) | sample_size=100, selection=first_n | MRR@5 | 0.079 |
| Full Pipeline | MedMCQA (train) | sample_size=50, selection=first_n | Top-1 accuracy | 0.28 (14/50) |

Artifact files:

- `data/processed/evaluation/vision_ham10000_eval.json`
- `data/processed/evaluation/vision_ham10000_eval.md`
- `data/processed/evaluation/rag_medqa_mrr_eval.json`
- `data/processed/evaluation/rag_medqa_mrr_eval.md`
- `data/processed/evaluation/pipeline_medmcqa_accuracy_eval.json`
- `data/processed/evaluation/pipeline_medmcqa_accuracy_eval.md`

Sample manual test inputs:

- `data/sample_inputs/sample_med_image.jpg`
- `data/sample_inputs/sample_lab_report.pdf`

## 10) Testing

Run all tests from repository root:

```bash
pytest -q
```

Representative coverage includes:

- API contract and endpoint tests
- PDF parser behavior
- RAG agent behavior
- report and vision agent behavior
- end-to-end pipeline checks

## 11) Configuration

Environment values are loaded from `.env` (see `.env.example`).

Common settings:

- `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- `OLLAMA_MODEL` (default `llama3.1:8b`)
- `VISION_MODEL` (default `llava:13b`)
- `CHROMADB_PATH` (default `./data/chromadb`)
- `CORS_ORIGINS`
- `LOG_LEVEL`

## 12) Known Limitations

- This is a prototype for portfolio/education, not production clinical deployment.
- Quality varies with model availability and prompt behavior.
- Evaluation runs are currently small-sample and should be expanded for stronger claims.
- Docker Compose exists but is not fully wired as the default full-stack runtime.

## 13) Troubleshooting

If frontend cannot reach backend:

- ensure backend is running on `127.0.0.1:8000`
- confirm Vite dev server is on `127.0.0.1:3000`
- verify proxy config in `frontend/vite.config.js`

If health is degraded:

- verify Ollama is up and serving tags endpoint
- verify Chroma path is writable (`CHROMADB_PATH`)

If ngrok URL is unavailable:

- restart with `scripts/start_demo_stack.ps1`
- check `ngrok_runtime.log` and `ngrok_runtime.err.log`

## 14) Project Documentation and Tracking

- docs index: `docs/README.md`
- architecture and implementation notes: `docs/CLAUDE.md`
- product requirements: `docs/PRD.md`
- prompt library: `docs/PROMPTS.md`
- execution log and benchmark history: `docs/progress.md`
- phase tracker: `docs/TODO.md`

## 15) Clinical Disclaimer

MediAgent is a clinical decision support prototype for educational and portfolio use.
It does not replace professional medical judgment, diagnosis, or treatment decisions.
