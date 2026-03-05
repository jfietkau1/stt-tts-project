from __future__ import annotations

import httpx


class XTTSv2TTS:
    """HTTP client for an XTTS v2 TTS service.

    Expects an endpoint:
        POST /tts
        Body JSON: {"text": "...", "language": "en", "speaker_wav": "..."}
        Response: WAV audio bytes
    """

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint.rstrip("/")

    def synthesize(
        self, text: str, *, language: str = "en", voice: str | None = None
    ) -> bytes:
        url = f"{self._endpoint}/tts"

        payload: dict[str, str] = {
            "text": text,
            "language": language,
        }
        if voice:
            payload["speaker_wav"] = voice

        response = httpx.post(url, json=payload, timeout=120.0)
        response.raise_for_status()

        return response.content
