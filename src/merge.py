import shutil
import subprocess
import tempfile
from pathlib import Path


def merge_audio_files(audio_files: list[Path], output_path: Path | str) -> Path:
    if not audio_files:
        raise ValueError("No audio files were provided for merging")

    # ffmpeg must be installed locally and available on PATH.
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise RuntimeError("ffmpeg was not found on PATH")

    final_output = Path(output_path)
    final_output.parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg concat mode reads a text file that lists each input file.
    concat_file = write_concat_file(audio_files, final_output.parent)
    try:
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
                str(final_output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.strip() or "ffmpeg failed to merge audio files") from error
    finally:
        concat_file.unlink(missing_ok=True)

    return final_output


def write_concat_file(audio_files: list[Path], directory: Path) -> Path:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        prefix="ffmpeg_concat_",
        dir=directory,
        delete=False,
    ) as handle:
        for audio_file in audio_files:
            handle.write(f"file '{escape_ffmpeg_path(audio_file.resolve())}'\n")

    return Path(handle.name)


def escape_ffmpeg_path(path: Path) -> str:
    return path.as_posix().replace("'", r"'\''")
