# TODO.md — MediAgent Phased Task Tracker

> **How to use:** Work top to bottom. Each phase must be 100% complete before the next.  
> Mark tasks: `[ ]` → `[x]` when done.

---

## Phase 0 — Project Scaffolding & Environment

### Repo & Environment
- [ ] Create GitHub repo `mediagent`
- [ ] Initialize Python 3.11 virtual environment
- [ ] Create `requirements.txt` with all dependencies
- [ ] Create `.env.example` and `.env` (gitignored)
- [ ] Create folder structure as defined in `CLAUDE.md`
- [ ] Initialize `docker-compose.yml` with Ollama + ChromaDB services
- [ ] Add `.gitignore` (venv, .env, data/raw, __pycache__, *.pyc)

### Ollama Setup
- [ ] Install Ollama locally (`https://ollama.com`)
- [ ] Pull `llama3.1:8b` model
- [ ] Pull `llava:13b` model (or `llava:7b` if RAM < 16GB)
- [ ] Test Ollama API: `curl http://localhost:11434/api/tags`

### ChromaDB Setup
- [ ] Install ChromaDB (`pip install chromadb`)
- [ ] Create `backend/rag/vectorstore.py` with collection init
- [ ] Create three collections: `medqa_chunks`, `pubmed_abstracts`, `medical_guidelines`
- [ ] Write and test `scripts/setup_chromadb.py`

### FastAPI Skeleton
- [ ] Create `backend/main.py` with `GET /api/health` endpoint
- [ ] Create `backend/config.py` with env var loading
- [ ] Create `backend/models/schemas.py` with all Pydantic models
- [ ] Test: `uvicorn backend.main:app --reload` runs without error

**Phase 0 Done When:** `GET /api/health` returns `{"status": "ok", "ollama": true, "chromadb": true}`

---

## Phase 1 — Individual Agents

### Vision Agent
- [ ] Create `backend/tools/image_loader.py`
  - [ ] PIL image loading and resizing
  - [ ] Basic image validation (is it a medical image heuristic)
  - [ ] Base64 encoding for Ollama multimodal API
- [ ] Create `backend/agents/vision_agent.py`
  - [ ] LLaVA call via `langchain-ollama` `ChatOllama` with image support
  - [ ] Structured output parsing → `VisionFindings` Pydantic schema
  - [ ] Error handling for non-medical / unreadable images
- [ ] Write `VISION_AGENT_PROMPT` in `PROMPTS.md`
- [ ] Unit test: `tests/test_vision_agent.py`
  - [ ] Test with sample chest X-ray PNG
  - [ ] Test with a random non-medical image (should return warning)

### PDF Parser Tool
- [ ] Create `backend/tools/pdf_parser.py`
  - [ ] PyMuPDF text extraction
  - [ ] Table extraction from lab reports
  - [ ] OCR fallback with pytesseract for scanned PDFs
  - [ ] Returns structured `LabReport` Pydantic object

### RAG Agent
- [ ] Create `backend/rag/embedder.py`
  - [ ] Load `pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb` from HuggingFace
  - [ ] `embed_texts(texts: list[str]) -> list[list[float]]` function
- [ ] Create `scripts/ingest_medqa.py`
  - [ ] Load `bigbio/med_qa` from HuggingFace datasets
  - [ ] Chunk into 512-token segments
  - [ ] Embed with BioBERT and upsert to `medqa_chunks` ChromaDB collection
- [ ] Create `backend/tools/pubmed_tool.py`
  - [ ] NCBI E-utilities API search (`esearch` + `efetch`)
  - [ ] Returns top-5 abstract texts with PMID and title
  - [ ] Rate limit: max 3 requests/second
- [ ] Create `backend/agents/rag_agent.py`
  - [ ] ChromaDB retriever (top-5 chunks)
  - [ ] PubMed API tool call
  - [ ] Context merging and deduplication
  - [ ] Returns `RAGContext` Pydantic schema
- [ ] Write `RAG_AGENT_PROMPT` in `PROMPTS.md`
- [ ] Unit test: `tests/test_rag_agent.py`
  - [ ] Test with symptom: "fever, cough, bilateral chest pain"
  - [ ] Verify at least 3 relevant conditions returned

**Phase 1 Done When:** Both agents return valid Pydantic objects when called individually.

---

## Phase 2 — LangGraph Orchestration

### State & Graph Definition
- [ ] Create `backend/agents/orchestrator.py`
  - [ ] Define `MediAgentState` TypedDict
  - [ ] Define `StateGraph` with nodes: `vision_node`, `rag_node`, `report_node`
  - [ ] Wire edges: `START → vision_node → rag_node → report_node → END`
  - [ ] Add conditional edge: skip `vision_node` if no image provided
  - [ ] Compile graph with `graph.compile()`

### Report Agent
- [ ] Create `backend/agents/report_agent.py`
  - [ ] Accepts merged Vision + RAG state
  - [ ] LLaMA 3.1 8B call via Ollama
  - [ ] Structured output → `ClinicalReport` Pydantic schema
  - [ ] ICD-10 code mapping (use static dict for top-50 conditions)
  - [ ] Disclaimer injection (always appended, never skippable)
- [ ] Write `REPORT_AGENT_PROMPT` in `PROMPTS.md`

### Integration Test
- [ ] Run full pipeline test in `tests/test_pipeline.py`
  - [ ] Input: sample X-ray + "chest pain and fever" text
  - [ ] Verify `ClinicalReport` schema returned
  - [ ] Verify disclaimer present
  - [ ] Verify at least 1 differential diagnosis with ICD-10 code

**Phase 2 Done When:** Full pipeline returns a valid `ClinicalReport` JSON from a test script.

---

## Phase 3 — FastAPI Complete

### Core Endpoints
- [ ] `POST /api/analyze`
  - [ ] Accept `multipart/form-data`: image (optional), pdf (optional), symptoms (string), voice (optional)
  - [ ] Save to temp dir `{session_id}/`
  - [ ] Initialize and run LangGraph
  - [ ] Return `ClinicalReport` JSON
  - [ ] Delete temp files after response
- [ ] `POST /api/transcribe`
  - [ ] Load Whisper `base` model
  - [ ] Accept audio file, return transcription text
- [ ] `GET /api/models/status`
  - [ ] Ping Ollama for each model
  - [ ] Return `{llama3: bool, llava: bool, whisper: bool, chromadb: bool}`
- [ ] `GET /api/export/{session_id}`
  - [ ] Return report as PDF using PyMuPDF
  - [ ] Return report as Markdown
  - [ ] Return report as JSON

### CORS & Middleware
- [ ] Add CORS middleware (allow `localhost:3000`)
- [ ] Add request logging middleware
- [ ] Add global exception handler returning clean error JSON

### LangSmith Tracing
- [ ] Add `LANGCHAIN_TRACING_V2=true` to env
- [ ] Add `LANGSMITH_API_KEY` to env
- [ ] Verify traces appear in LangSmith dashboard

**Phase 3 Done When:** Postman/curl can hit `/api/analyze` with a real image and get a valid JSON response.

---

## Phase 4 — Frontend Integration (Google Stitch → React)

### Stitch Generation
- [ ] Use `STITCH.md` prompt to generate UI in Google Stitch
- [ ] Export React components from Stitch
- [ ] Set up React project in `frontend/`

### Frontend Components
- [ ] `InputPanel` — Image dropzone, PDF upload, symptom text, voice recorder
- [ ] `VoiceRecorder` — MediaRecorder API, waveform visualization, Whisper transcription display
- [ ] `ResultsPanel` — Tabbed: Summary | Diagnoses | Evidence | Next Steps
- [ ] `DiagnosisCard` — Condition name, ICD badge, confidence radial, expandable evidence
- [ ] `RedFlagBanner` — High-contrast alert for urgent findings
- [ ] `SourceChip` — Clickable PubMed citation chips
- [ ] `TraceViewer` — Collapsible LangSmith trace timeline
- [ ] `StatusBar` — Model loading status indicators
- [ ] `ExportBar` — PDF / MD / JSON export buttons

### API Integration
- [ ] Create `src/api/client.js` with axios instance
- [ ] `analyzePatient(formData)` → POST `/api/analyze`
- [ ] `transcribeVoice(audioBlob)` → POST `/api/transcribe`
- [ ] `getModelsStatus()` → GET `/api/models/status`
- [ ] Loading states for all async calls
- [ ] Error boundary with user-friendly messages

**Phase 4 Done When:** Full demo works — upload image + type symptoms → see formatted report in browser.

---

## Phase 5 — Polish, Eval & Portfolio Readiness

### Evaluation
- [ ] Run Vision Agent on 50 HAM10000 skin images → record accuracy
- [ ] Run RAG Agent on 100 MedQA questions → record MRR@5
- [ ] Run full pipeline on 50 MedMCQA questions → record accuracy
- [ ] Document all results in `README.md`

### README
- [ ] Project banner / demo GIF
- [ ] Architecture diagram (from `CLAUDE.md`)
- [ ] Quick start instructions
- [ ] Benchmark results table
- [ ] Tech stack badges
- [ ] "How it works" section with agent explanation
- [ ] Disclaimer section

### Demo Prep
- [ ] Record 2-minute Loom demo video
- [ ] Deploy backend on Railway or Render (free tier)
- [ ] Deploy frontend on Vercel
- [ ] Add live demo link to README and resume

### Resume Line
- [ ] Add to resume: *"Built MediAgent, a multimodal clinical decision support system using a 3-agent LangGraph pipeline (LLaVA + BioBERT RAG + LLaMA 3.1), achieving X% accuracy on MedMCQA benchmark with zero external API dependencies"*

**Phase 5 Done When:** GitHub repo is public, demo is live, README is complete.
