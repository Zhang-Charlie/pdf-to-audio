import shutil
import subprocess
import tempfile
from pathlib import Path


def merge_audio_files(audio_files: list[Path], output_path: Path) -> Path:
    if not audio_files:
        raise ValueError("No audio files were provided for merging")

    # Look for ffmpeg on the system PATH.
    # We use ffmpeg because it is a simple, reliable local tool for media work.
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise RuntimeError("ffmpeg was not found on PATH")

    # Create the output folder if needed.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg concat mode expects a text file listing the input files.
    concat_file = _write_concat_file(audio_files, output_path.parent)
    try:
        # Run ffmpeg and overwrite the output file if it already exists.
        # We merge into WAV using pcm_s16le, a common uncompressed WAV codec.
        subprocess.run(
            [
                ffmpeg_path,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c:a",
                "pcm_s16le",
                str(output_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        # Bubble up ffmpeg's own error message so debugging is easier.
        raise RuntimeError(error.stderr.strip() or "ffmpeg failed to merge audio files") from error
    finally:
        # The concat list is temporary, so clean it up after the merge.
        concat_file.unlink(missing_ok=True)

    return output_path


def _write_concat_file(audio_files: list[Path], directory: Path) -> Path:
    # Create a temporary text file in the output directory.
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        prefix="ffmpeg_concat_",
        dir=directory,
        delete=False,
    ) as handle:
        for audio_file in audio_files:
            # Each line tells ffmpeg to include one input file.
            handle.write(f"file '{_escape_for_ffmpeg(audio_file.resolve())}'\n")

    return Path(handle.name)


def _escape_for_ffmpeg(path: Path) -> str:
    # ffmpeg concat files use single quotes around paths.
    # If a path itself contains a quote, escape it safely.
    return path.as_posix().replace("'", r"'\''")
