"""
embedding the user query
search chunks
return the text from the best chunks

"""

from app.processing.embeddings import embed_text
from app.db.db import search_chunks


def retrieve_relevant_chunks(query: str, k=5):
    print("retrieve_relevant_chunks is running")
    query_embedding = embed_text(query)
    rows = search_chunks(query_embedding, k)
    return rows
