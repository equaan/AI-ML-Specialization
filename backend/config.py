from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = "MediAgent"
    api_prefix: str = "/api"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    vision_model: str = os.getenv("VISION_MODEL", "llava:7b")
    chromadb_path: str = os.getenv("CHROMADB_PATH", "./data/chromadb")
    pubmed_api_key: str | None = os.getenv("PUBMED_API_KEY") or None
    langsmith_api_key: str | None = os.getenv("LANGSMITH_API_KEY") or None
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "mediagent")
    langsmith_enabled: bool = os.getenv("LANGSMITH_ENABLED", "false").lower() == "true"
    langchain_tracing_v2: bool = False
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cors_origins: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        object.__setattr__(self, "cors_origins", _split_csv(origins))
        Path(self.chromadb_path).mkdir(parents=True, exist_ok=True)
        tracing_requested = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        tracing_enabled = self.langsmith_enabled and tracing_requested and bool(self.langsmith_api_key)
        object.__setattr__(self, "langchain_tracing_v2", tracing_enabled)
        if not tracing_enabled:
            os.environ["LANGCHAIN_TRACING_V2"] = "false"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
