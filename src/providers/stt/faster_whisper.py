from __future__ import annotations

import httpx


class FasterWhisperSTT:
    """HTTP client for a Faster Whisper transcription service.

    Expects an OpenAI-compatible whisper endpoint:
        POST /v1/audio/transcriptions
        Body: multipart form with "file" (audio) and optional "language"
        Response: {"text": "..."}
    """

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint.rstrip("/")

    def transcribe(self, audio: bytes, *, language: str | None = None) -> str:
        url = f"{self._endpoint}/v1/audio/transcriptions"

        files = {"file": ("audio.wav", audio, "audio/wav")}
        data: dict[str, str] = {}
        if language:
            data["language"] = language

        response = httpx.post(url, files=files, data=data, timeout=60.0)
        response.raise_for_status()

        return response.json().get("text", "").strip()
