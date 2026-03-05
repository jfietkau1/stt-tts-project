from __future__ import annotations

import io

import numpy as np
import sounddevice as sd
import soundfile as sf


def play_audio(audio_bytes: bytes) -> None:
    """Play WAV audio bytes through the default output device."""
    audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")
    sd.play(audio_data, samplerate=sample_rate)
    sd.wait()
