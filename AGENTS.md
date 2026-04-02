# Build a simple Python app that converts a PDF into audio.

Pipeline:
PDF -> extract -> clean -> chunk -> TTS -> merge

Rules:

- Keep everything simple and local
- No Redis, queues, APIs, or distributed systems
- Use PyMuPDF for extraction
- Use regex for cleaning
- Use local TTS
- Use ffmpeg for merging

Guidelines:

- One file per step (extract, clean, chunk, tts, merge)
- Small, clear functions
- Do not overengineer
- Focus on correctness, not performance

Goal:
Produce a working CLI tool:
python src/main.py input.pdf
