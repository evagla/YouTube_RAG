"""
Semantic chunker with overlap
"""

import re  # RegEx


def chunk_text(text: str, max_chars: int = 500, overlap: int = 100):

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
