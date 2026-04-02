import re


# A line that only contains digits is often a page number like "12".
PAGE_NUMBER_PATTERN = re.compile(r"(?m)^\s*\d+\s*$")

# PDFs often split words across lines:
# exam-
# ple
# This pattern lets us turn that back into "example".
HYPHENATED_LINE_BREAK_PATTERN = re.compile(r"(\w)-\n(\w)")

# A single newline inside a paragraph usually should become a space.
# Double newlines are treated as paragraph breaks and are preserved.
SINGLE_LINE_BREAK_PATTERN = re.compile(r"(?<!\n)\n(?!\n)")

# Collapse runs of spaces and tabs into one normal space.
MULTI_SPACE_PATTERN = re.compile(r"[ \t]+")

# Remove awkward spaces before punctuation like "word ," -> "word,"
SPACE_BEFORE_PUNCTUATION_PATTERN = re.compile(r"\s+([,.;:!?])")

# If we end up with lots of blank lines, shrink them down.
MULTI_BLANK_LINE_PATTERN = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    # Normalize different newline styles to "\n".
    # Windows often uses \r\n while some files may contain \r.
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove simple page numbers on their own lines.
    cleaned = PAGE_NUMBER_PATTERN.sub("", cleaned)

    # Fix words broken by a hyphen at the end of a line.
    cleaned = HYPHENATED_LINE_BREAK_PATTERN.sub(r"\1\2", cleaned)

    # Turn single line breaks into spaces so sentences flow normally.
    cleaned = SINGLE_LINE_BREAK_PATTERN.sub(" ", cleaned)

    # Remove extra spaces and tabs.
    cleaned = MULTI_SPACE_PATTERN.sub(" ", cleaned)

    # Remove spaces before punctuation marks.
    cleaned = SPACE_BEFORE_PUNCTUATION_PATTERN.sub(r"\1", cleaned)

    # Reduce large blank gaps to normal paragraph spacing.
    cleaned = MULTI_BLANK_LINE_PATTERN.sub("\n\n", cleaned)

    # Strip leading and trailing whitespace from the final result.
    return cleaned.strip()
