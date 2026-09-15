from app.ingestion.youtube import fetch_transcript
from app.db.db import (
    insert_video,
    insert_transcript,
    insert_chunk,
    get_connection,
    get_transcript_id_for_video,
    video_has_metadata,
    insert_playlist_video,
)
from app.processing.chunking import chunk_text
from app.processing.embeddings import embed_text
from app.ingestion.youtube_metadata_ingestion import ingest_metadata
from app.ingestion.youtube_metadata import fetch_playlist_video_ids


def ingest_video(video_id: str) -> int | None:
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
        print(
            f"[INFO] Transcript not found  in local database. Fetching from YouTube pipeline..."
        )

    # 2 . Try to fetch transcript BEFORE involving the db
    try:
        print(f"[INFO] Fetching transcript for video '{video_id}'")
        transcript_text = fetch_transcript(video_id)

        if not transcript_text:
            raise ValueError("Transcript text is empty or None")

    except Exception as e:
        print(
            f"[WARNING] Could not fetch transcript for video '{video_id}'. Skipping. Error: {e}"
        )
        return None

    # 3. Create db record for video with fully fetched transcript
    vid = insert_video(video_id)

    # Fetch metadata for video
    try:
        print(f"[INFO] Fetching metadata for new video...")
        ingest_metadata(video_id)
    except Exception as meta_error:
        print(
            f"[WARNING] Metadata extraction failed or warned, but continuing transcript storage Error: {meta_error}"
        )

    # 4. Fetch transcript
    # transcript_text = fetch_transcript(video_id)

    # 5. Insert transcript row
    transcript_id = insert_transcript(vid, transcript_text)

    # 6. Chunk transcript
    chunks = chunk_text(transcript_text)

    # 7. Insert chunks
    for idx, chunk in enumerate(chunks):
        insert_chunk(transcript_id, idx, chunk)

    # 8. Embed chunks
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


def ingest_playlist(playlist_url: str) -> list[int]:
    """
    Playlist ingestion pipeline:
    -Extract all video IDs form the playlist URL
    -Loop through each videoID and run the exisistng ingest_video pipeline,
     and link the video to the playlist in the playlist_video table.
    Retuns: A list of transcript_ids that were successfullly processed
    """

    print(f"\n[INFO] Starting playlist ingestion pipeline...")

    # 1. fetch playlist_id from URL
    playlist_id = "unknown_playlist"
    if "list=" in playlist_url:
        playlist_id = playlist_url.split("list=")[1].split("&")[0]

    # 12. Fetch all video IDs from palylist
    try:
        video_ids = fetch_playlist_video_ids(playlist_url)
    except Exception as e:
        print(f"[ERROR] Colud not extract video IDs from palylist. Error: {e}")
        return []

    successful_transcript_ids = []

    # 3. Loop thorugh the list of video IDs and run the pipeline
    for idx, video_id in enumerate(video_ids, start=1):
        print(f"\n--- Processing playlist video '{idx}''/''{len(video_ids)}'---")

        transcript_id = ingest_video(video_id)

        if transcript_id is not None:
            successful_transcript_ids.append(transcript_id)

            # 4. get for the internal db id for the video
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "SELECT id FROM videos WHERE youtube_id = %s", (video_id,)
                        )
                        row = cur.fetchone()
                        if row:
                            video_db_id = row[0]
                            insert_playlist_video(playlist_id, video_db_id)
                            print(
                                f"[INFO] Linked video '{video_id}' to playlist '{playlist_id}' in database."
                            )
            except Exception as db_err:
                print(
                    f"[WARNING] Could not link video '{video_id}' to playlist. Error: {db_err}"
                )

        else:
            print(
                f"[WARNING] skipping '{video_id}' in playlist due to ingestion failure."
            )

    print(
        f"\n[INFO] Playlist ingestion finished. Sucessfully processed {len(successful_transcript_ids)} out of {len(video_ids)} videos"
    )
    return successful_transcript_ids
