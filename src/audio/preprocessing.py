from __future__ import annotations

import io

import numpy as np
import soundfile as sf


def preprocess_audio(
    audio_bytes: bytes,
    target_sample_rate: int = 16000,
    target_channels: int = 1,
    normalize: bool = True,
) -> bytes:
    """Prepare raw audio for STT consumption.

    - Converts to mono if needed
    - Resamples to target sample rate (linear interpolation -- sufficient
      when source and target rates are close or identical, which is the
      common case since we record at 16 kHz already)
    - Peak-normalizes volume to 95% to avoid clipping
    """
    audio_data, source_rate = sf.read(io.BytesIO(audio_bytes), dtype="float32")

    if audio_data.ndim > 1 and target_channels == 1:
        audio_data = np.mean(audio_data, axis=1)

    if source_rate != target_sample_rate:
        ratio = target_sample_rate / source_rate
        new_length = int(len(audio_data) * ratio)
        indices = np.linspace(0, len(audio_data) - 1, new_length)
        audio_data = np.interp(
            indices, np.arange(len(audio_data)), audio_data
        ).astype(np.float32)

    if normalize:
        peak = np.max(np.abs(audio_data))
        if peak > 0:
            audio_data = audio_data / peak * 0.95

    buf = io.BytesIO()
    sf.write(buf, audio_data, target_sample_rate, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()
