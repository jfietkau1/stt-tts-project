from __future__ import annotations

from src.config import AppConfig
from src.core.stt_interface import STTProvider
from src.core.tts_interface import TTSProvider
from src.providers.stt.faster_whisper import FasterWhisperSTT
from src.providers.tts.fish_speech import FishSpeechTTS
from src.providers.tts.xtts_v2 import XTTSv2TTS

_STT_REGISTRY: dict[str, type] = {
    "faster-whisper": FasterWhisperSTT,
}

_TTS_REGISTRY: dict[str, type] = {
    "xtts-v2": XTTSv2TTS,
    "fish-speech": FishSpeechTTS,
}


def create_stt_provider(config: AppConfig) -> STTProvider:
    name = config.stt.provider
    if name not in _STT_REGISTRY:
        available = ", ".join(_STT_REGISTRY)
        raise ValueError(f"Unknown STT provider '{name}'. Available: {available}")

    return _STT_REGISTRY[name](endpoint=config.stt.endpoint)


def create_tts_provider(config: AppConfig) -> TTSProvider:
    name = config.tts.provider
    if name not in _TTS_REGISTRY:
        available = ", ".join(_TTS_REGISTRY)
        raise ValueError(f"Unknown TTS provider '{name}'. Available: {available}")

    return _TTS_REGISTRY[name](endpoint=config.tts.endpoint)
