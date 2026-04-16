from __future__ import annotations

import tempfile
import time
from pathlib import Path

import httpx
import fitz
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.orchestrator import MediAgentOrchestrator
from backend.config import Settings, get_settings
from backend.models.schemas import HealthStatus, ModelStatus
from backend.rag.vectorstore import chromadb_is_healthy
from backend.tools.pdf_parser import PDFParser
from backend.tools.voice_input import VoiceInputProcessor
from backend.utils.helpers import generate_session_id
from backend.utils.logger import get_logger
from backend.utils.report_store import report_store


settings = get_settings()
logger = get_logger(__name__)
orchestrator = MediAgentOrchestrator()
pdf_parser = PDFParser()
voice_processor = VoiceInputProcessor()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Multimodal clinical decision support backend for MediAgent.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def ollama_is_healthy() -> bool:
    url = f"{settings.ollama_base_url.rstrip('/')}/api/tags"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
        return True
    except Exception as exc:  # pragma: no cover - network-dependent
        logger.warning("Ollama health check failed: %s", exc)
        return False


async def get_model_status(settings_obj: Settings) -> ModelStatus:
    url = f"{settings_obj.ollama_base_url.rstrip('/')}/api/tags"
    model_names: set[str] = set()
    ollama_ok = False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            payload = response.json()
            model_names = {item.get("name", "") for item in payload.get("models", [])}
            ollama_ok = True
    except Exception:
        ollama_ok = False

    return ModelStatus(
        llama3=ollama_ok and settings_obj.ollama_model in model_names,
        llava=ollama_ok and settings_obj.vision_model in model_names,
        whisper=False,
        chromadb=chromadb_is_healthy(),
    )


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info("%s %s -> %s (%sms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception for %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Something went wrong while processing the request.",
        },
    )


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    return {"message": "MediAgent API is running"}


@app.get(f"{settings.api_prefix}/health", response_model=HealthStatus, tags=["system"])
async def health_check() -> HealthStatus:
    model_status = await get_model_status(settings)
    ollama_ok = model_status.llama3
    chroma_ok = model_status.chromadb

    if ollama_ok and chroma_ok:
        return HealthStatus(status="ok", ollama=True, chromadb=True, message="All core services reachable.")

    return HealthStatus(
        status="degraded",
        ollama=ollama_ok,
        chromadb=chroma_ok,
        message="One or more local dependencies are unavailable. See logs for details.",
    )


@app.get(f"{settings.api_prefix}/models/status", response_model=ModelStatus, tags=["system"])
async def models_status() -> ModelStatus:
    return await get_model_status(settings)


@app.get("/health", response_model=HealthStatus, tags=["system"])
async def health_check_compat() -> HealthStatus:
    # Compatibility alias for demo scripts and tunnel probes.
    return await health_check()


@app.get("/stats", tags=["system"])
async def stats_compat() -> dict:
    # Compatibility endpoint for quick tunnel checks.
    model_status = await get_model_status(settings)
    return {
        "status": "ok",
        "services": {
            "llama3": model_status.llama3,
            "llava": model_status.llava,
            "whisper": model_status.whisper,
            "chromadb": model_status.chromadb,
        },
    }


@app.post(f"{settings.api_prefix}/transcribe", tags=["analysis"])
async def transcribe_audio(audio: UploadFile = File(...)) -> dict[str, str]:
    suffix = Path(audio.filename or "audio.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        content = await audio.read()
        temp_audio.write(content)
        temp_path = Path(temp_audio.name)

    try:
        transcript = voice_processor.transcribe(temp_path)
        return {"transcript": transcript}
    finally:
        temp_path.unlink(missing_ok=True)


@app.post(f"{settings.api_prefix}/analyze", tags=["analysis"])
async def analyze_patient(
    symptoms: str = Form(""),
    image: UploadFile | None = File(default=None),
    pdf: UploadFile | None = File(default=None),
    voice: UploadFile | None = File(default=None),
) -> dict:
    if not any([symptoms.strip(), image, pdf, voice]):
        raise HTTPException(status_code=400, detail="At least one input is required.")

    session_id = generate_session_id()
    with tempfile.TemporaryDirectory(prefix=f"mediagent-{session_id}-") as temp_dir:
        temp_root = Path(temp_dir)
        image_path = await _save_upload(image, temp_root) if image else None
        pdf_path = await _save_upload(pdf, temp_root) if pdf else None
        voice_path = await _save_upload(voice, temp_root) if voice else None

        voice_transcript = voice_processor.transcribe(voice_path) if voice_path else None
        parsed_lab_report = _parse_pdf_report(pdf_path) if pdf_path else None
        pdf_summary = _summarize_lab_report(parsed_lab_report) if parsed_lab_report else ""

        combined_symptoms = "\n".join(
            part for part in [symptoms.strip(), voice_transcript or "", pdf_summary] if part
        )

        result = orchestrator.run(
            {
                "patient_symptoms": combined_symptoms,
                "image_path": str(image_path) if image_path else None,
                "pdf_path": str(pdf_path) if pdf_path else None,
                "voice_transcript": voice_transcript,
                "messages": [],
            }
        )

    final_report = result.get("final_report")
    if not final_report:
        raise HTTPException(status_code=500, detail="Analysis completed without a final report.")

    report_store.save(
        session_id=session_id,
        report=final_report,
        lab_report=parsed_lab_report.model_dump() if parsed_lab_report else None,
        inputs={
            "symptoms": symptoms,
            "image_name": image.filename if image else None,
            "pdf_name": pdf.filename if pdf else None,
            "voice_name": voice.filename if voice else None,
        },
    )
    return {
        "session_id": session_id,
        "report": final_report,
        "lab_report": parsed_lab_report.model_dump() if parsed_lab_report else None,
    }


@app.get(f"{settings.api_prefix}/reports", tags=["analysis"])
async def list_reports(limit: int = 25) -> dict[str, list[dict]]:
    items = report_store.list_recent(limit=limit)
    return {"reports": items}


@app.get(f"{settings.api_prefix}/reports/{{session_id}}", tags=["analysis"])
async def get_report(session_id: str) -> dict:
    item = report_store.get_full(session_id)
    if not item:
        raise HTTPException(status_code=404, detail="Session report not found.")
    return item


@app.get(f"{settings.api_prefix}/export/{{session_id}}", tags=["analysis"])
async def export_report(session_id: str, format: str = "json") -> Response:
    report = report_store.get(session_id)
    if not report:
        raise HTTPException(status_code=404, detail="Session report not found.")

    normalized = format.lower()
    if normalized == "json":
        return JSONResponse(content=report)
    if normalized == "markdown":
        return PlainTextResponse(content=_report_to_markdown(report), media_type="text/markdown")
    if normalized == "pdf":
        pdf_bytes = _report_to_pdf_bytes(report)
        headers = {"Content-Disposition": f'attachment; filename="{session_id}.pdf"'}
        return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
    raise HTTPException(status_code=400, detail="Unsupported export format. Use json, markdown, or pdf.")


async def _save_upload(upload: UploadFile, temp_root: Path) -> Path:
    filename = upload.filename or "upload.bin"
    destination = temp_root / filename
    content = await upload.read()
    destination.write_bytes(content)
    return destination


def _parse_pdf_report(pdf_path: Path | None):
    if not pdf_path:
        return None
    try:
        return pdf_parser.parse_lab_report(pdf_path)
    except Exception as exc:
        logger.warning("PDF parsing failed: %s", exc)
        return None


def _summarize_lab_report(parsed_lab_report) -> str:
    return f"Lab report type: {parsed_lab_report.report_type}. Key tests: " + ", ".join(
        f"{result.test_name}={result.value}" for result in parsed_lab_report.test_results[:5]
    )


def _report_to_markdown(report: dict) -> str:
    lines = [
        "# MediAgent Clinical Report",
        "",
        "## Patient Summary",
        report.get("patient_summary", ""),
        "",
        "## Differential Diagnosis",
    ]
    for diagnosis in report.get("differential_diagnosis", []):
        lines.append(
            f"- Rank {diagnosis.get('rank')}: {diagnosis.get('condition')} "
            f"({diagnosis.get('icd_10_code')}) - confidence {diagnosis.get('confidence_score')}"
        )
    lines.extend(["", "## Red Flags"])
    for flag in report.get("red_flags", []):
        lines.append(f"- {flag}")
    lines.extend(["", "## Recommended Next Steps"])
    for step in report.get("recommended_next_steps", []):
        lines.append(f"- {step}")
    lines.extend(["", "## Disclaimer", report.get("disclaimer", "")])
    return "\n".join(lines)


def _report_to_pdf_bytes(report: dict) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    text = _report_to_markdown(report)
    page.insert_textbox(fitz.Rect(40, 40, 555, 800), text, fontsize=11)
    return doc.tobytes()
