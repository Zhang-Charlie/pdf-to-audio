import time
from pathlib import Path


def synthesize_chunks(chunks: list[str], output_dir: Path, rate: int = 180) -> list[Path]:
    # Import inside the function for the same reason as extract.py:
    # the CLI can still start and show help even if pyttsx3 is missing.
    import pyttsx3

    if not chunks:
        raise ValueError("No chunks were provided for TTS")

    # Make sure the output folder exists before writing audio files.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the local text-to-speech engine and configure the speaking speed.
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    audio_files: list[Path] = []
    try:
        for index, chunk in enumerate(chunks, start=1):
            # Use zero-padded filenames so they stay in the correct order.
            # Example: chunk_0001.wav, chunk_0002.wav
            output_path = output_dir / f"chunk_{index:04d}.wav"

            # Queue this text for speech synthesis into a WAV file.
            engine.save_to_file(chunk, str(output_path))

            # Actually run the queued synthesis job.
            engine.runAndWait()

            # Some engines return before the file is fully visible on disk.
            # Wait until the file exists and has content.
            _wait_for_file(output_path)
            audio_files.append(output_path)
    finally:
        # Stop the engine cleanly even if an error happens.
        engine.stop()

    return audio_files


def _wait_for_file(path: Path, timeout_seconds: float = 10.0) -> None:
    # Keep checking the filesystem for a short time.
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size > 0:
            return
        time.sleep(0.1)

    # If the file never appears, surface a clear error.
    raise RuntimeError(f"TTS output was not created: {path}")
