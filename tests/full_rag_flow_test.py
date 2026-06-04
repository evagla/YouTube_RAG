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
"""

from app.rag.rag_pipeline import run_rag
from app.ingestion.youtube_ingestion import ingest_video
from app.db.db import get_transcript_id_for_video

# ---------------------------------------
# CONFIGURATION FOR THIS TEST
# ---------------------------------------

# 1. Set the YouTube video ID you want to test
VIDEO_ID = "KzpUJa4abzs"

# 2. Set the question you want to ask about the video
QUESTION = "What is the main topic of the video?"

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
    else:
        print(
            "transcript already exisits in DB (id = {transcript_id}). Skipping ingest.\n"
        )

    # 2. Run RAG
    print("Running RAG pipeline...\n")
    answer = run_rag(QUESTION, VIDEO_ID)

    print("=== RAG ANSWER ===\n")
    print(answer)
    print("\n===================\n")


if __name__ == "__main__":
    test_full_rag_flow()
