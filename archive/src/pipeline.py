from app.processing.chunking import chunk_text
from app.processing.embeddings import embed_text
from app.db.db import insert_chunk


def embed_and_store_text(transcript_id: str, text: str):

    print("embed_and_store pipeline initialized")

    """
    Take text, chunk, create embeddings and store in db.
    return listof chink-IDs 
    """
    chunks = chunk_text(text)
    saved_ids = []

    for idx, chunk in enumerate(chunks):
        print(f"creates embedding for chunk {idx}")
        embedding = embed_text(chunk)

        print(f" saving chunk {idx} in db...")
        chunk_id = insert_chunk(
            transcript_id=transcript_id,
            chunk_index=idx,
            text=chunk,
            embedding=embedding,
        )
        saved_ids.append(chunk_id)

    print("done")
    return saved_ids
