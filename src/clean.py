import re


# PDFs often split a word across lines like:
# exam-
# ple
# This regex turns that back into "example".
HYPHENATED_WORD_PATTERN = re.compile(r"(\w)-\s*\n\s*(\w)")

# A single newline inside a paragraph is usually just a wrapped line,
# not a real paragraph break. Double newlines are left alone.
BROKEN_LINE_BREAK_PATTERN = re.compile(r"(?<!\n)\n(?!\n)")

# Replace runs of spaces or tabs with one normal space.
EXTRA_SPACES_PATTERN = re.compile(r"[ \t]+")

# Clean up spaces around newline characters.
SPACES_AROUND_NEWLINES_PATTERN = re.compile(r" *\n *")

# If there are too many blank lines, reduce them to one empty line.
MULTI_BLANK_LINES_PATTERN = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    # Run the text through each cleaning step in order.
    cleaned = normalize_line_endings(text)
    cleaned = fix_hyphenated_words(cleaned)
    cleaned = fix_broken_line_breaks(cleaned)
    cleaned = remove_extra_spaces(cleaned)
    return cleaned


def normalize_line_endings(text: str) -> str:
    # Convert Windows and old-style line endings into "\n".
    return text.replace("\r\n", "\n").replace("\r", "\n")


def fix_hyphenated_words(text: str) -> str:
    # Join words broken by a hyphen at the end of a line.
    return HYPHENATED_WORD_PATTERN.sub(r"\1\2", text)


def fix_broken_line_breaks(text: str) -> str:
    # Turn wrapped lines inside a paragraph into spaces.
    return BROKEN_LINE_BREAK_PATTERN.sub(" ", text)


def remove_extra_spaces(text: str) -> str:
    # Collapse repeated spaces and tabs.
    cleaned = EXTRA_SPACES_PATTERN.sub(" ", text)

    # Remove extra spaces that sit directly next to newlines.
    cleaned = SPACES_AROUND_NEWLINES_PATTERN.sub("\n", cleaned)

    # Keep paragraph spacing simple and consistent.
    cleaned = MULTI_BLANK_LINES_PATTERN.sub("\n\n", cleaned)

    # Remove whitespace at the very start and end of the final text.
    return cleaned.strip()
