from __future__ import annotations

import logging

import click

from src.audio.capture import record_audio
from src.audio.playback import play_audio
from src.audio.preprocessing import preprocess_audio
from src.config import load_config
from src.factory import create_stt_provider, create_tts_provider

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


@click.group()
@click.option(
    "--config",
    "config_path",
    default=None,
    help="Path to settings YAML file.",
)
@click.pass_context
def main(ctx: click.Context, config_path: str | None) -> None:
    """STT/TTS client with pluggable providers."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_path)


@main.command()
@click.option(
    "--language",
    default=None,
    help="Language code (e.g. en, ru, es). Overrides config.",
)
@click.pass_context
def stt(ctx: click.Context, language: str | None) -> None:
    """Record from microphone and transcribe via the configured STT provider."""
    config = ctx.obj["config"]

    provider = create_stt_provider(config)
    lang = language or (
        config.stt.language if config.stt.language != "auto" else None
    )

    logger.info("STT provider: %s @ %s", config.stt.provider, config.stt.endpoint)

    raw_audio = record_audio(
        sample_rate=config.audio.sample_rate,
        channels=config.audio.channels,
        silence_threshold=config.audio.silence_threshold,
        silence_duration_ms=config.audio.silence_duration_ms,
        max_record_seconds=config.audio.max_record_seconds,
    )

    if not raw_audio:
        click.echo("No audio captured.")
        return

    audio = preprocess_audio(
        raw_audio,
        target_sample_rate=config.audio.sample_rate,
        target_channels=config.audio.channels,
    )

    logger.info("Transcribing %d bytes of audio...", len(audio))
    text = provider.transcribe(audio, language=lang)

    click.echo(f"\nTranscription: {text}")
    logger.info("Result: %s", text)


@main.command()
@click.argument("text")
@click.option(
    "--language",
    default=None,
    help="Language code (e.g. en, ru, es). Overrides config.",
)
@click.option(
    "--voice",
    default=None,
    help="Voice identifier. Overrides config.",
)
@click.pass_context
def tts(ctx: click.Context, text: str, language: str | None, voice: str | None) -> None:
    """Synthesize text to speech and play through speakers."""
    config = ctx.obj["config"]

    provider = create_tts_provider(config)
    lang = language or config.tts.language
    voice_id = voice or config.tts.voice

    logger.info("TTS provider: %s @ %s", config.tts.provider, config.tts.endpoint)
    logger.info("Synthesizing: %s", text)

    audio = provider.synthesize(text, language=lang, voice=voice_id)

    if not audio:
        click.echo("No audio returned from TTS provider.")
        return

    play_audio(audio)
    logger.info("Playback complete.")


if __name__ == "__main__":
    main()
