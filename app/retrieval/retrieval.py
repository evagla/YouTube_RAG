"""
embedding the user query
search chunks
return the text from the best chunks

"""

# -------------------------------------------
# Retrieve based on specified youtube video
# -------------------------------------------
from app.processing.embeddings import embed_text
from app.db.db import (
    get_transcript_id_for_video,
    search_chunks_for_transcript,
)


def retrieve_relevant_chunks(query: str, youtube_id: str, k=5):
    print("retrieve_relevant_chunks is running")

    # 1.Get transcript_id for the video
    transcript_id = get_transcript_id_for_video(youtube_id)
    if transcript_id is None:
        raise Exception(f"No transcript found for video {youtube_id}")

    # 2. Embed query
    query_embedding = embed_text(query)

    # 3. Serch chunks for this transcript ONLY
    rows = search_chunks_for_transcript(transcript_id, query_embedding, k)
    return rows


def retrieve_texts(query: str, youtube_id: str, k=5):
    rows = retrieve_relevant_chunks(query, youtube_id, k)
    return [row["text"] for row in rows]


'''

# -------------------------------------------
# Retrieve from all videos in db
# -------------------------------------------
from app.processing.embeddings import embed_text
from app.db.db import search_chunks


def retrieve_relevant_chunks(query: str, k=5):
    print("retrieve_relevant_chunks is running")
    query_embedding = embed_text(query)
    rows = search_chunks(query_embedding, k)
    return rows



def retrieve_texts(query: str, k: int = 5) -> list[str]:
    """
    Returns only the text fields from the retrieved chunks.
    """
    rows = retrieve_relevant_chunks(query, k)
    return [row["text"] for row in rows]
'''
