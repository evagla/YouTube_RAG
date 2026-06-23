"""
Semantic chunker with overlap
"""

import re  # RegEx
from config.config import load_settings

settings = load_settings()
chunk_config = settings.get("chunking", {})

# get parameters dynamically with fallbacks
DEFAULT_MAX_CHARS = chunk_config.get("max_chars", 500)
DEFAULT_OVERLAP = chunk_config.get("overlap", 100)


def chunk_text(text: str, max_chars: int = None, overlap: int = None):
    # Fallbackvalues included, if needed
    if max_chars is None:
        max_chars = DEFAULT_MAX_CHARS
    if overlap is None:
        overlap = DEFAULT_OVERLAP

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current = ""

    for sentence in sentences:
        # If a whole sentence will make the chunk to big -> save the chunk
        if len(current) + len(sentence) + 1 > max_chars:
            chunks.append(current.strip())
            # Start a new chunk with overlap
            current = current[-overlap:] + " " + sentence
        else:
            current += " " + sentence

    # The last chunk
    if current.strip():
        chunks.append(current.strip())

    return chunks
