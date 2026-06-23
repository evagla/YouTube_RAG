"""
embedding the user query
search chunks
return the text from the best chunks

"""

from app.processing.embeddings import embed_text
from app.db.db import (
    get_transcript_id_for_video,
    search_chunks_for_transcript,
)
from app.retrieval.query_expansion import expand_query
from app.retrieval.reranker import rerank
from config.config import load_settings

settings = load_settings()
retrieval_config = settings.get("retrieval", {})

# creating global constants with fallbacks
DEFAULT_TOP_K = retrieval_config.get("top_k", 5)
DEFAULT_CANDIDATES = retrieval_config.get("candidates", 15)
DEFAULT_TRUNCATE_LENGTH = retrieval_config.get("truncate_length", 300)


def retrieve_relevant_chunks(expanded_query: str, youtube_id: str, k=None):
    print("...Retrieving relevant chunks...")

    # fall back if needed
    if k is None:
        k = DEFAULT_TOP_K

    # 1.Get transcript_id for the video
    transcript_id = get_transcript_id_for_video(youtube_id)
    if transcript_id is None:
        raise Exception(f"No transcript found for video {youtube_id}")

    # 2. Embed query
    query_embedding = embed_text(expanded_query)

    # 3 A. Get top 15 candidates
    candidates = search_chunks_for_transcript(
        transcript_id, query_embedding, DEFAULT_CANDIDATES
    )

    # 3 B. Truncate long chunk text before reranking
    for row in candidates:
        if len(row["text"]) > DEFAULT_TRUNCATE_LENGTH:
            row["text"] = row["text"][:DEFAULT_TRUNCATE_LENGTH]

    # 3 C. Rerank the candidates
    reranked = rerank(expanded_query, candidates, top_k=k)

    return reranked


def retrieve_texts(query: str, youtube_id: str, k=5):
    # expanded query
    expanded_query = expand_query(query)

    # retrieve chunks incl reranker scores
    rows = retrieve_relevant_chunks(expanded_query, youtube_id, k)

    # return a structured result for run_rag()
    return {
        "original_query": query,
        "expanded_query": expanded_query,
        "chunks": rows,
        "retrieval_confidence": rows[0]["score"] if rows else None,
    }


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
