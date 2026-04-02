from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    # Import the PDF library inside the function.
    # That way, the program can still show --help even if the dependency
    # is not installed yet.
    import fitz

    # Fail early if the file path is wrong.
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # This tool is only meant for PDFs.
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {pdf_path}")

    # We collect page text here and join it at the end.
    pages: list[str] = []
    with fitz.open(str(pdf_path)) as document:
        # Read the document one page at a time.
        for page in document:
            # "text" asks PyMuPDF for plain text from the page.
            page_text = page.get_text("text").strip()

            # Skip completely empty pages.
            if page_text:
                pages.append(page_text)

    # Separate pages with blank lines so paragraph structure is easier
    # to preserve in later steps.
    return "\n\n".join(pages)
