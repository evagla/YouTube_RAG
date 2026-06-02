from app.db.db import get_chunks_for_transcript, update_chunk_embedding
from app.processing.embeddings import embed_text

TRANSCRIPT_ID = 3


def run_embedding_test():
    print(f"Fetching chunks for transcript_id={TRANSCRIPT_ID}...")
    rows = get_chunks_for_transcript(TRANSCRIPT_ID)

    print(f"Found {len(rows)} chunks. Start embedding...\n")

    for chunk_id, text in rows:
        print(f"  → embeding chunk {chunk_id}...")
        embedding = embed_text(text)
        update_chunk_embedding(chunk_id, embedding)

    print("\nDONE! All embeddings are saved to the database.")


if __name__ == "__main__":
    run_embedding_test()
