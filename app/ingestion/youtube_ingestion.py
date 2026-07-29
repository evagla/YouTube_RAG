from app.ingestion.youtube import fetch_transcript
from app.db.db import (
    insert_video,
    insert_transcript,
    insert_chunk,
    get_connection,
    get_transcript_id_for_video,
    video_has_metadata,
)
from app.processing.chunking import chunk_text
from app.processing.embeddings import embed_text
from app.ingestion.youtube_metadata_ingestion import ingest_metadata


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
    # Check if the video transcript already exists in the database
    print(f"[INFO] Processing video_id: {video_id}")
    # 1. Is the video_id already in the db?
    transcript_id = get_transcript_id_for_video(video_id)

    if transcript_id is not None:
        #  A: Skipp donwload if present, check metadata
        print(
            f"[INFO] Video '{video_id}' already exisits in database. Skipping ingestion. Checking for metadata..."
        )

        # Check metadata for video_id
        if not video_has_metadata(video_id):
            # download metadata if not present
            print(f"[INFO] Metadata missing for '{video_id}'. Fetching metadata...")
            ingest_metadata(video_id)

        # ingest_video is done
        return transcript_id

    else:
        # B: Download video and metadata
        print(f"[INFO] Transcript not found. Running transcript pipeline...")

    # Create db record
    vid = insert_video(video_id)
    # Fetch metadata for video
    print(f"[INFO] Fetching metadat for new video...")
    ingest_metadata(video_id)

    # 2. Fetch transcript
    transcript_text = fetch_transcript(video_id)

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
