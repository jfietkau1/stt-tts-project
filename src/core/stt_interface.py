from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class STTProvider(Protocol):
    """Interface that all STT provider implementations must satisfy."""

    def transcribe(self, audio: bytes, *, language: str | None = None) -> str:
        """Transcribe audio bytes to text.

        Args:
            audio: WAV audio data as bytes (16kHz, mono, 16-bit PCM).
            language: Optional language code (e.g. "en", "ru", "es").
                      None means auto-detect.

        Returns:
            Transcribed text.
        """
        ...
