# PDF to Audio

Simple local CLI tool that converts a PDF into speech.

Pipeline:

PDF -> extract -> clean -> chunk -> TTS -> merge

## Requirements

- Python 3.10+
- `ffmpeg` installed and available on `PATH`

## Install

```bash
python -m pip install -r requirements.txt
```

## Usage

```bash
python src/main.py input.pdf
```

The final audio file is written to:

```text
output/<pdf-name>/<pdf-name>.wav
```

Chunk audio files are stored in:

```text
output/<pdf-name>/chunks/
```

## Modules

- `src/extract.py`: PDF text extraction with PyMuPDF
- `src/clean.py`: regex-based cleanup
- `src/chunk.py`: sentence-aware chunking
- `src/tts.py`: local speech synthesis with `pyttsx3`
- `src/merge.py`: final merge with `ffmpeg`
- `src/main.py`: CLI entrypoint
