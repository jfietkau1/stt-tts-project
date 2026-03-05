from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TTSProvider(Protocol):
    """Interface that all TTS provider implementations must satisfy."""

    def synthesize(
        self, text: str, *, language: str = "en", voice: str | None = None
    ) -> bytes:
        """Synthesize text to speech audio.

        Args:
            text: The text to synthesize.
            language: Language code (e.g. "en", "ru", "es").
            voice: Optional voice identifier. Meaning is provider-specific
                   (could be a speaker embedding name, a reference audio path, etc.).

        Returns:
            WAV audio data as bytes.
        """
        ...
