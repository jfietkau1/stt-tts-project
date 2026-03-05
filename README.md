# STT/TTS Project

A pluggable Speech-to-Text and Text-to-Speech client with configurable providers.

## Architecture

This project is a **client application** that calls remote STT and TTS services running on a GPU server. The models themselves (Faster Whisper, XTTS v2, Fish Speech) run as separate services -- this project handles audio capture, preprocessing, and provider communication.

### Supported Providers

**STT:**
- Faster Whisper (via HTTP, OpenAI-compatible API)

**TTS:**
- XTTS v2 (via HTTP)
- Fish Speech (via HTTP)

Providers are swappable via configuration -- no code changes needed.

## Setup

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/settings.yaml` to point to your GPU server's service endpoints:

```yaml
stt:
  provider: "faster-whisper"
  endpoint: "http://your-gpu-server:8001"

tts:
  provider: "xtts-v2"    # or "fish-speech"
  endpoint: "http://your-gpu-server:8002"
```

### Environment Variable Overrides

- `STT_ENDPOINT` -- Override the STT service endpoint
- `TTS_ENDPOINT` -- Override the TTS service endpoint
- `STT_TTS_CONFIG` -- Path to a custom config file

## Usage

### Transcribe speech (STT)

```bash
python -m src.cli stt
```

Records from your microphone until silence is detected, sends to the configured STT service, and prints the transcription.

```bash
python -m src.cli stt --language en
```

### Synthesize speech (TTS)

```bash
python -m src.cli tts "Hello, this is a test"
```

Sends text to the configured TTS service and plays the resulting audio through your speakers.

```bash
python -m src.cli tts "Hola mundo" --language es --voice spanish_speaker
```

### Global Options

```bash
python -m src.cli --config path/to/config.yaml stt
```
