from __future__ import annotations

import io

import numpy as np
import sounddevice as sd
import soundfile as sf


def record_audio(
    sample_rate: int = 16000,
    channels: int = 1,
    silence_threshold: float = 0.01,
    silence_duration_ms: int = 1000,
    max_record_seconds: int = 30,
) -> bytes:
    """Record audio from the microphone until silence is detected.

    Uses energy-based voice activity detection: once speech is detected
    (RMS above threshold), recording continues until RMS stays below the
    threshold for ``silence_duration_ms`` milliseconds.

    Returns empty bytes if no speech is detected before the timeout.
    """
    chunk_ms = 100
    chunk_samples = int(sample_rate * chunk_ms / 1000)
    silence_chunks_needed = int(silence_duration_ms / chunk_ms)
    max_chunks = int(max_record_seconds * 1000 / chunk_ms)

    audio_chunks: list[np.ndarray] = []
    silence_counter = 0
    speech_detected = False

    print("Listening... (speak now)")

    with sd.InputStream(
        samplerate=sample_rate, channels=channels, dtype="float32"
    ) as stream:
        for _ in range(max_chunks):
            chunk, _ = stream.read(chunk_samples)
            audio_chunks.append(chunk.copy())

            rms = float(np.sqrt(np.mean(chunk**2)))

            if rms > silence_threshold:
                speech_detected = True
                silence_counter = 0
            elif speech_detected:
                silence_counter += 1
                if silence_counter >= silence_chunks_needed:
                    break

    if not speech_detected:
        print("No speech detected.")
        return b""

    print("Recording complete.")

    audio_data = np.concatenate(audio_chunks, axis=0)

    buf = io.BytesIO()
    sf.write(buf, audio_data, sample_rate, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()
