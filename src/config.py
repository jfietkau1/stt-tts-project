from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class STTConfig:
    provider: str = "faster-whisper"
    endpoint: str = "http://localhost:8001"
    language: str = "auto"


@dataclass
class TTSConfig:
    provider: str = "xtts-v2"
    endpoint: str = "http://localhost:8002"
    voice: str = "default"
    language: str = "en"


@dataclass
class AudioConfig:
    sample_rate: int = 16000
    channels: int = 1
    silence_threshold: float = 0.01
    silence_duration_ms: int = 1000
    max_record_seconds: int = 30


@dataclass
class AppConfig:
    stt: STTConfig = field(default_factory=STTConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)


def _filter_fields(data: dict, cls: type) -> dict:
    valid = {f.name for f in cls.__dataclass_fields__.values()}
    return {k: v for k, v in data.items() if k in valid}


def load_config(config_path: str | None = None) -> AppConfig:
    if config_path is None:
        config_path = os.environ.get(
            "STT_TTS_CONFIG",
            str(Path(__file__).parent.parent / "config" / "settings.yaml"),
        )

    path = Path(config_path)
    if not path.exists():
        return AppConfig()

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    stt_data = raw.get("stt", {})
    tts_data = raw.get("tts", {})
    audio_data = raw.get("audio", {})

    if env_stt := os.environ.get("STT_ENDPOINT"):
        stt_data["endpoint"] = env_stt
    if env_tts := os.environ.get("TTS_ENDPOINT"):
        tts_data["endpoint"] = env_tts

    return AppConfig(
        stt=STTConfig(**_filter_fields(stt_data, STTConfig)),
        tts=TTSConfig(**_filter_fields(tts_data, TTSConfig)),
        audio=AudioConfig(**_filter_fields(audio_data, AudioConfig)),
    )
