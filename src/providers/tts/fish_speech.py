from __future__ import annotations

import httpx


class FishSpeechTTS:
    """HTTP client for a Fish Speech TTS service.

    Expects an endpoint:
        POST /v1/tts
        Body JSON: {"text": "...", "language": "en", "reference_id": "..."}
        Response: WAV audio bytes
    """

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint.rstrip("/")

    def synthesize(
        self, text: str, *, language: str = "en", voice: str | None = None
    ) -> bytes:
        url = f"{self._endpoint}/v1/tts"

        payload: dict[str, str] = {
            "text": text,
            "language": language,
        }
        if voice:
            payload["reference_id"] = voice

        response = httpx.post(url, json=payload, timeout=120.0)
        response.raise_for_status()

        return response.content
