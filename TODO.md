# TODO.md - MediAgent Phased Task Tracker

> How to use: Work top to bottom. Each phase must be 100% complete before the next.
> Mark tasks: `[ ]` -> `[x]` when done.

---

## Phase 0 - Project Scaffolding & Environment

### Repo & Environment
- [ ] Create GitHub repo `mediagent`
- [ ] Initialize Python 3.11 virtual environment
- [x] Create `requirements.txt` with all dependencies
- [x] Create `.env.example` and `.env` (gitignored)
- [x] Create folder structure as defined in `CLAUDE.md`
- [x] Initialize `docker-compose.yml` with Ollama + ChromaDB services
- [x] Add `.gitignore` (venv, .env, data/raw, __pycache__, *.pyc)

### Ollama Setup
- [ ] Install Ollama locally (`https://ollama.com`)
- [ ] Pull `llama3.1:8b` model
- [ ] Pull `llava:13b` model (or `llava:7b` if RAM < 16GB)
- [ ] Test Ollama API: `curl http://localhost:11434/api/tags`

### ChromaDB Setup
- [ ] Install ChromaDB (`pip install chromadb`)
- [x] Create `backend/rag/vectorstore.py` with collection init
- [x] Create three collections: `medqa_chunks`, `pubmed_abstracts`, `medical_guidelines`
- [ ] Write and test `scripts/setup_chromadb.py`

### FastAPI Skeleton
- [x] Create `backend/main.py` with `GET /api/health` endpoint
- [x] Create `backend/config.py` with env var loading
- [x] Create `backend/models/schemas.py` with all Pydantic models
- [ ] Test: `uvicorn backend.main:app --reload` runs without error

Phase 0 Done When: `GET /api/health` returns `{"status": "ok", "ollama": true, "chromadb": true}`

---

## Phase 1 - Individual Agents

### Vision Agent
- [x] Create `backend/tools/image_loader.py`
  - [x] PIL image loading and resizing
  - [x] Basic image validation (is it a medical image heuristic)
  - [x] Base64 encoding for Ollama multimodal API
- [x] Create `backend/agents/vision_agent.py`
  - [x] LLaVA call via `langchain-ollama` `ChatOllama` with image support
  - [x] Structured output parsing -> `VisionFindings` Pydantic schema
  - [x] Error handling for non-medical / unreadable images
- [ ] Write `VISION_AGENT_PROMPT` in `PROMPTS.md`
- [ ] Unit test: `tests/test_vision_agent.py`
  - [ ] Test with sample chest X-ray PNG
  - [ ] Test with a random non-medical image (should return warning)

### PDF Parser Tool
- [x] Create `backend/tools/pdf_parser.py`
  - [x] PyMuPDF text extraction
  - [x] Table extraction from lab reports
  - [x] OCR fallback with pytesseract for scanned PDFs
  - [x] Returns structured `LabReport` Pydantic object

### RAG Agent
- [x] Create `backend/rag/embedder.py`
  - [x] Load `pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb` from HuggingFace
  - [x] `embed_texts(texts: list[str]) -> list[list[float]]` function
- [x] Create `scripts/ingest_medqa.py`
  - [x] Load `bigbio/med_qa` from HuggingFace datasets
  - [x] Chunk into 512-token segments
  - [x] Embed with BioBERT and upsert to `medqa_chunks` ChromaDB collection
- [x] Create `backend/tools/pubmed_tool.py`
  - [x] NCBI E-utilities API search (`esearch` + `efetch`)
  - [x] Returns top-5 abstract texts with PMID and title
  - [x] Rate limit: max 3 requests/second
- [x] Create `backend/agents/rag_agent.py`
  - [x] ChromaDB retriever (top-5 chunks)
  - [x] PubMed API tool call
  - [x] Context merging and deduplication
  - [x] Returns `RAGContext` Pydantic schema
- [ ] Write `RAG_AGENT_PROMPT` in `PROMPTS.md`
- [ ] Unit test: `tests/test_rag_agent.py`
  - [ ] Test with symptom: "fever, cough, bilateral chest pain"
  - [ ] Verify at least 3 relevant conditions returned

Phase 1 Done When: Both agents return valid Pydantic objects when called individually.

---

## Phase 2 - LangGraph Orchestration

### State & Graph Definition
- [x] Create `backend/agents/orchestrator.py`
  - [x] Define `MediAgentState` TypedDict
  - [x] Define `StateGraph` with nodes: `vision_node`, `rag_node`, `report_node`
  - [x] Wire edges: `START -> vision_node -> rag_node -> report_node -> END`
  - [x] Add conditional edge: skip `vision_node` if no image provided
  - [x] Compile graph with `graph.compile()`

### Report Agent
- [x] Create `backend/agents/report_agent.py`
  - [x] Accepts merged Vision + RAG state
  - [ ] LLaMA 3.1 8B call via Ollama
  - [x] Structured output -> `ClinicalReport` Pydantic schema
  - [x] ICD-10 code mapping (use static dict for top-50 conditions)
  - [x] Disclaimer injection (always appended, never skippable)
- [ ] Write `REPORT_AGENT_PROMPT` in `PROMPTS.md`

### Integration Test
- [ ] Run full pipeline test in `tests/test_pipeline.py`
  - [ ] Input: sample X-ray + "chest pain and fever" text
  - [ ] Verify `ClinicalReport` schema returned
  - [ ] Verify disclaimer present
  - [ ] Verify at least 1 differential diagnosis with ICD-10 code

Phase 2 Done When: Full pipeline returns a valid `ClinicalReport` JSON from a test script.

---

## Phase 3 - FastAPI Complete

### Core Endpoints
- [x] `POST /api/analyze`
  - [x] Accept `multipart/form-data`: image (optional), pdf (optional), symptoms (string), voice (optional)
  - [x] Save to temp dir `{session_id}/`
  - [x] Initialize and run LangGraph
  - [x] Return `ClinicalReport` JSON
  - [x] Delete temp files after response
- [x] `POST /api/transcribe`
  - [x] Load Whisper `base` model
  - [x] Accept audio file, return transcription text
- [x] `GET /api/models/status`
  - [x] Ping Ollama for each model
  - [x] Return `{llama3: bool, llava: bool, whisper: bool, chromadb: bool}`
- [x] `GET /api/export/{session_id}`
  - [x] Return report as PDF using PyMuPDF
  - [x] Return report as Markdown
  - [x] Return report as JSON

### CORS & Middleware
- [x] Add CORS middleware (allow `localhost:3000`)
- [x] Add request logging middleware
- [x] Add global exception handler returning clean error JSON

### LangSmith Tracing
- [ ] Add `LANGCHAIN_TRACING_V2=true` to env
- [ ] Add `LANGSMITH_API_KEY` to env
- [ ] Verify traces appear in LangSmith dashboard

Phase 3 Done When: Postman/curl can hit `/api/analyze` with a real image and get a valid JSON response.

---

## Phase 4 - Frontend Integration (Google Stitch -> React)

### Stitch Generation
- [ ] Use `STITCH.md` prompt to generate UI in Google Stitch
- [ ] Export React components from Stitch
- [x] Set up React project in `frontend/`

### Frontend Components
- [x] `InputPanel` - Image dropzone, PDF upload, symptom text, voice recorder
- [x] `VoiceRecorder` - MediaRecorder API, waveform visualization, Whisper transcription display
- [x] `ResultsPanel` - Tabbed: Summary | Diagnoses | Evidence | Next Steps
- [x] `DiagnosisCard` - Condition name, ICD badge, confidence radial, expandable evidence
- [x] `RedFlagBanner` - High-contrast alert for urgent findings
- [x] `SourceChip` - Clickable PubMed citation chips
- [x] `TraceViewer` - Collapsible LangSmith trace timeline
- [x] `StatusBar` - Model loading status indicators
- [x] `ExportBar` - PDF / MD / JSON export buttons

### API Integration
- [x] Create `src/api/client.js` with axios instance
- [x] `analyzePatient(formData)` -> POST `/api/analyze`
- [x] `transcribeVoice(audioBlob)` -> POST `/api/transcribe`
- [x] `getModelsStatus()` -> GET `/api/models/status`
- [x] Loading states for all async calls
- [x] Error boundary with user-friendly messages

Phase 4 Done When: Full demo works - upload image + type symptoms -> see formatted report in browser.

---

## Phase 5 - Polish, Eval & Portfolio Readiness

### Evaluation
- [ ] Run Vision Agent on 50 HAM10000 skin images -> record accuracy
- [ ] Run RAG Agent on 100 MedQA questions -> record MRR@5
- [ ] Run full pipeline on 50 MedMCQA questions -> record accuracy
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

Phase 5 Done When: GitHub repo is public, demo is live, README is complete.
