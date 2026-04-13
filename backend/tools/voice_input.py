from __future__ import annotations

from pathlib import Path

import whisper


class VoiceInputProcessor:
    def __init__(self, model_name: str = "base") -> None:
        self.model_name = model_name
        self._model = None

    def transcribe(self, audio_path: str | Path) -> str:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {path}")

        try:
            model = self._get_model()
            result = model.transcribe(str(path))
            text = (result.get("text") or "").strip()
            return self._cleanup_transcript(text)
        except Exception:
            return "Transcription fallback: Whisper model unavailable on this machine yet."

    def _get_model(self):
        if self._model is None:
            self._model = whisper.load_model(self.model_name)
        return self._model

    @staticmethod
    def _cleanup_transcript(text: str) -> str:
        return " ".join(text.split())
