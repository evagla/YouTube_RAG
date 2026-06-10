"""
FULL RAG PIPELINE TEST
======================

This test verifies that the entire RAG pipeline works end-to-end.

HOW TO USE THIS FILE
--------------------

1. Set the YouTube video ID you want to test:
       VIDEO_ID = "REPLACE_ME"

2. Run the ingest pipeline to download transcript, chunk it,
   embed it and store it in the database:
       uv run python -m app.ingest.ingest VIDEO_ID

3. Set your test question in the variable QUESTION below, or use the current one.

4. Run this test:
       uv run python -m tests.full_rag_flow_test

EXPECTED OUTPUT
---------------
- Retrieval logs (5 chunks)
- A clean answer from the LLM based strictly on the video content
- No errors from Ollama or the RAG pipeline

If the answer is coherent and based on the video, the RAG system works.

NOTE ABOUT YT-DLP WARNINGS
--------------------------

When this test runs, yt-dlp may print warnings such as:

- "No supported JavaScript runtime could be found"
- "ffmpeg not found"

These warnings are expected and harmless in this context.

The metadata ingestion step only extracts video metadata (title, channel,
upload date) and does NOT download or process video or audio streams.
Therefore, yt-dlp works correctly even without a JS runtime or ffmpeg.

The warnings can be ignored during testing.

"""

from app.rag.rag_pipeline import run_rag
from app.ingestion.youtube_ingestion import ingest_video
from app.db.db import get_transcript_id_for_video, video_has_metadata
from app.ingestion.youtube_metadata_ingestion import ingest_metadata

# ---------------------------------------
# CONFIGURATION FOR THIS TEST
# ---------------------------------------

# 1. Set the YouTube video ID you want to test
VIDEO_ID = "KzpUJa4abzs"

# 2. Set the question you want to ask about the video
QUESTION = "what color is the shirt?"

# ---------------------------------------
# RUN TEST
# ---------------------------------------


def test_full_rag_flow():
    print("\n=== FULL RAG PIPELINE TEST ===\n")
    print(f"Video ID: {VIDEO_ID}")
    print(f"Question: {QUESTION}\n")

    # 1. Check if viedo already ingested
    transcript_id = get_transcript_id_for_video(VIDEO_ID)
    if transcript_id is None:
        print("Transcript not found in DB. Running ingest pipeline...\n")
        ingest_video(VIDEO_ID)
    if not video_has_metadata(VIDEO_ID):
        print("Get metadata for video...")
        ingest_metadata(VIDEO_ID)
    else:
        print(
            f"transcript already exisits in DB (id = {transcript_id}). Skipping ingest.\n"
        )

    # 2. Run RAG
    print("# Running RAG pipeline...\n")
    answer = run_rag(QUESTION, VIDEO_ID)

    print("=== RAG ANSWER ===\n")
    print(answer)
    print("\n===================\n")


if __name__ == "__main__":
    test_full_rag_flow()
