from app.ingestion.youtube import fetch_transcript
from app.db.db import insert_video, insert_transcript, insert_chunk, get_connection
from app.processing.chunking import chunk_text
from app.processing.embeddings import embed_text


def ingest_video(video_id: str) -> int:
    """
    Full ingestion pipeline:
    - fetch transcript
    - insert video
    - insert transcript
    - chunk transcript
    - insert chunks
    - embed chunks
    Returns: transcript_id
    """

    # 1. Fetch transcript
    # transcript_text, metadata = fetch_transcript(video_id)
    transcript_text = fetch_transcript(video_id)

    # 2. Insert video row with metadata
    vid = insert_video(video_id)
    """vid = insert_video(
        youtube_id=video_id,
        title=metadata["title"],
        channel=metadata["channel"],
        published_at=metadata["published_at"],
    )"""

    # 3. Insert transcript row
    transcript_id = insert_transcript(vid, transcript_text)

    # 4. Chunk transcript
    chunks = chunk_text(transcript_text)

    # 5. Insert chunks
    for idx, chunk in enumerate(chunks):
        insert_chunk(transcript_id, idx, chunk)

    # 6. Embed chunks
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, text FROM chunks WHERE transcript_id = %s ORDER BY id",
                (transcript_id,),
            )
            rows = cur.fetchall()

    for chunk_id, text in rows:
        embedding = embed_text(text)
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE chunks SET embedding = %s WHERE id = %s",
                    (embedding, chunk_id),
                )
                conn.commit()

    return transcript_id
