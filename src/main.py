import argparse
from pathlib import Path

# Each step in the pipeline lives in its own file.
# We import the small helper functions here and call them in order.
from chunk import chunk_text
from clean import clean_text
from extract import extract_text_from_pdf
from merge import merge_audio_files
from tts import synthesize_chunks


def main() -> int:
    # argparse builds a small command-line interface for us.
    # This lets the user run:
    # python src/main.py input.pdf
    parser = argparse.ArgumentParser(description="Convert a PDF into spoken audio.")

    # The PDF path is the required positional argument.
    parser.add_argument("pdf", help="Path to the input PDF")

    # The output directory is optional.
    # If the user does not pass it, we use "output".
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where audio files should be written",
    )
    args = parser.parse_args()

    # Convert user input into absolute paths so the rest of the code
    # works with clear, unambiguous file locations.
    pdf_path = Path(args.pdf).expanduser().resolve()
    output_root = Path(args.output_dir).expanduser().resolve()

    # We create one folder per PDF so each run stays organized.
    # Example:
    # output/my_book/
    job_dir = output_root / pdf_path.stem

    # Individual chunk audio files go here.
    chunk_dir = job_dir / "chunks"

    # This is the final merged audio file.
    final_audio_path = job_dir / f"{pdf_path.stem}.wav"

    # Step 1: read text from the PDF.
    print(f"Extracting text from {pdf_path}...")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Step 2: clean up messy PDF text so speech sounds better.
    print("Cleaning text...")
    cleaned_text = clean_text(extracted_text)

    # If nothing useful is left, stop early with a clear error.
    if not cleaned_text:
        raise RuntimeError("The PDF did not produce any readable text after cleaning")

    # Step 3: split the text into smaller pieces.
    # TTS tools are more reliable with smaller chunks than one giant string.
    print("Chunking text...")
    chunks = chunk_text(cleaned_text)

    # This should not happen if cleaning worked, but we check anyway.
    if not chunks:
        raise RuntimeError("The cleaned text could not be split into chunks")

    # Step 4: generate one audio file per text chunk.
    print(f"Generating audio for {len(chunks)} chunk(s)...")
    audio_files = synthesize_chunks(chunks, chunk_dir)

    # Step 5: merge all chunk files into one final WAV file.
    print("Merging audio...")
    merge_audio_files(audio_files, final_audio_path)

    # Tell the user where the finished file lives.
    print(f"Done: {final_audio_path}")
    return 0


if __name__ == "__main__":
    # This makes the file runnable as a script from the command line.
    raise SystemExit(main())
