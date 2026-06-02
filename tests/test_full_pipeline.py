from app.ingestion.youtube import fetch_transcript
from app.db.db import insert_transcript, insert_chunk, get_connection, insert_video
from app.processing.chunking import chunk_text
from app.processing.embeddings import embed_text

VIDEO_ID = "TP1IbL6doUY"


def run_full_pipeline():
    print("1.fetch transcript from yputube")
    transcript_text = fetch_transcript(VIDEO_ID)
    print(" -> Fetched Transcript, length :", len(transcript_text))

    print("1. Creating video entry...")
    video_id = insert_video(VIDEO_ID)
    print(" -> viedo_id:", video_id)

    print("\n2. Inserting transcript to database...")
    transcript_id = insert_transcript(video_id, transcript_text)
    print(" -> Inserted using transcript_id:", transcript_id)

    print("\3n. Chunking transcripts...")
    chunks = chunk_text(transcript_text)
    print(" -> Number of chunks:", len(chunks))

    print("\n4. Inserting chunks to database...")
    for idx, chunk in enumerate(chunks):
        insert_chunk(transcript_id, idx, chunk)
    print(" -> Chunks inserted")

    print("\n5. Embedding chunks...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, text FROM chunks WHERE transcript_id = %s ORDER BY id",
                (transcript_id,),
            )
            rows = cur.fetchall()

    for chunnk_id, text in rows:
        embedding = embed_text(text)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE chunks SET embedding = %s WHERE id = %s",
                    (embedding, chunnk_id),
                )
                conn.commit()

    print(" -> Embeddings Inserted")

    print("\n6. Verifying...")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM chunks WHERE transcript_id = %s AND embedding IS NOT NULL",
                (transcript_id,),
            )
            count = cur.fetchone()[0]

    print(f" -> {count} chunks now has embedding.")
    print("\nDONE! The whole pipe is working.")


if __name__ == "__main__":
    run_full_pipeline()
