import time
from pathlib import Path


def synthesize_chunks(
    chunks: list[str],
    output_dir: Path | str = Path("output"),
    rate: int = 180,
) -> list[Path]:
    # Import inside the function so the rest of the CLI can still load
    # even if the TTS dependency is not installed yet.
    import pyttsx3

    if not chunks:
        raise ValueError("No chunks were provided for TTS")

    # Always write chunk audio files under output/ by default.
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    audio_files: list[Path] = []
    try:
        for index, chunk in enumerate(chunks, start=1):
            audio_file = output_path / f"chunk_{index:04d}.wav"
            synthesize_chunk(engine, chunk, audio_file)
            audio_files.append(audio_file)
    finally:
        engine.stop()

    return audio_files


def synthesize_chunk(engine, text: str, output_path: Path) -> None:
    # Convert one text chunk into one audio file.
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()
    wait_for_file(output_path)


def wait_for_file(path: Path, timeout_seconds: float = 10.0) -> None:
    # Some TTS engines finish a little before the file is fully visible on disk.
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size > 0:
            return
        time.sleep(0.1)

    raise RuntimeError(f"TTS output was not created: {path}")
