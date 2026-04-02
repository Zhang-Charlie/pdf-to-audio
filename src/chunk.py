import re


# Split on whitespace that comes after sentence-ending punctuation.
# This is a simple heuristic, not a full grammar parser.
SENTENCE_BOUNDARY_PATTERN = re.compile(r"(?<=[.!?])\s+")


def chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    # A chunk size of zero or less makes no sense.
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")

    # Double newlines represent paragraph boundaries after cleaning.
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        # First split each paragraph into sentence-sized pieces.
        for sentence in _split_paragraph(paragraph, max_chars):
            if not current:
                current = sentence
                continue

            # Try to add the next sentence to the current chunk.
            candidate = f"{current} {sentence}".strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                # If adding it would make the chunk too large,
                # save the current chunk and start a new one.
                chunks.append(current)
                current = sentence

    # Add the final unfinished chunk, if there is one.
    if current:
        chunks.append(current)

    return chunks


def _split_paragraph(paragraph: str, max_chars: int) -> list[str]:
    # Break a paragraph into sentences, trimming whitespace.
    sentences = [sentence.strip() for sentence in SENTENCE_BOUNDARY_PATTERN.split(paragraph) if sentence.strip()]
    parts: list[str] = []

    # If sentence splitting finds nothing useful, fall back to the full paragraph.
    for sentence in sentences or [paragraph]:
        if len(sentence) <= max_chars:
            parts.append(sentence)
        else:
            # Very long sentences still need to be broken down further.
            parts.extend(_split_long_text(sentence, max_chars))

    return parts


def _split_long_text(text: str, max_chars: int) -> list[str]:
    # Last-resort splitting: build chunks word by word.
    # This avoids cutting in the middle of a word.
    words = text.split()
    parts: list[str] = []
    current = ""

    for word in words:
        if not current:
            current = word
            continue

        candidate = f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            parts.append(current)
            current = word

    if current:
        parts.append(current)

    return parts
