from app.services.processing.chunking import chunk_text
from app.services.processing.embeddings import ebed_text
from app.services.db import insert_chunk


def embed_adn_store_text(video_di: str, text: st):

    print("embed_and_store pipeline initialized")

    """
    Take text, chunk, create embeddings and store in db.
    return listof chink-IDs 
    """
    chunks = chunk_text(text)
    saved_ids = []

    for idx, chunk in enumerate(chunks):
        print(f"creates embedding for chunk {idx}")
        embedding = emed_text(chunk)

        print(f" saving chunk {idx} in db...")
        chunk_id = insert_chunk(
            video_id=video_id, chunk_index=idx, text=chunk, embedding=embedding
        )
        saved_ids.append(chunk_id)

    print("done")
    return saved_ids
