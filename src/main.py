import argparse
from pathlib import Path

from chunk import chunk_text
from clean import clean_text
from extract import extract_text_from_pdf
from merge import merge_audio_files
from tts import synthesize_chunks


def run_pipeline(pdf_path: Path) -> Path:
    # Store all generated files under output/<pdf-name>/.
    output_dir = Path("output") / pdf_path.stem
    chunk_dir = output_dir / "chunks"
    final_audio_path = output_dir / f"{pdf_path.stem}.wav"

    print(f"Extracting text from {pdf_path}...")
    extracted_text = extract_text_from_pdf(pdf_path)

    print("Cleaning text...")
    cleaned_text = clean_text(extracted_text)
    if not cleaned_text:
        raise RuntimeError("No text was left after cleaning")

    print("Chunking text...")
    chunks = chunk_text(cleaned_text)
    if not chunks:
        raise RuntimeError("No chunks were created")

    print(f"Generating audio for {len(chunks)} chunk(s)...")
    audio_files = synthesize_chunks(chunks, chunk_dir)

    print("Merging audio...")
    return merge_audio_files(audio_files, final_audio_path)


def main() -> int:
    # The CLI matches the project goal:
    # python src/main.py input.pdf
    parser = argparse.ArgumentParser(description="Convert a PDF into audio.")
    parser.add_argument("pdf", help="Path to the input PDF")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    final_audio_path = run_pipeline(pdf_path)

    print(f"Done: {final_audio_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
