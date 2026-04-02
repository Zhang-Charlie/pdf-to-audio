import re


# Split text at sentence boundaries like ".", "!" or "?" followed by whitespace.
# This is a simple rule, but it works well enough for a basic local tool.
SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    # The chunk size must be a positive number.
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")

    # Break the text into sentences first so we do not cut them in half.
    sentences = split_into_sentences(text)
    chunks: list[str] = []
    current_chunk = ""

    for sentence in sentences:
        # Start a new chunk with the first sentence.
        if not current_chunk:
            current_chunk = sentence
            continue

        # Try to add the next full sentence to the current chunk.
        candidate = f"{current_chunk} {sentence}"
        if len(candidate) <= max_chars:
            current_chunk = candidate
        else:
            # If adding the sentence would make the chunk too large,
            # save the current chunk and start a new one.
            chunks.append(current_chunk)
            current_chunk = sentence

    # Add the final chunk after the loop ends.
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def split_into_sentences(text: str) -> list[str]:
    # Remove leading and trailing whitespace first.
    cleaned = text.strip()
    if not cleaned:
        return []

    # Split the text into sentences using punctuation as the boundary.
    # If the text has no sentence punctuation, this returns the whole text
    # as one chunk, which is still better than breaking a sentence apart.
    return [sentence.strip() for sentence in SENTENCE_PATTERN.split(cleaned) if sentence.strip()]
