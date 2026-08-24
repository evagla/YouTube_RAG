"""

FULL RAG PIPELINE TEST
======================

This script provides an interactive way to test the entire RAG pipeline
end‑to‑end using any YouTube video ID.

WHAT THIS SCRIPT DOES
---------------------
- Generates a unique session ID for each run (clean conversation history)
- Ensures the video is ingested (transcript, metadata, chunks, embeddings)
- Starts an interactive question loop where you can ask multiple questions
  about the same video without reloading or re‑ingesting anything
- Uses the full RAG pipeline: retrieval → reranking → context building → LLM

HOW TO USE
----------
1. Run the script:
       uv run python -m scripts.full_rag_flow_test

2. Enter a YouTube video ID when prompted.

3. Ask questions about the video.
   Type "quit", "exit", or "kill" to stop.

EXPECTED BEHAVIOR
-----------------
- The script ingests the video only if needed.
- Retrieval and reranking logs appear for each question.
- The LLM answers strictly based on the video content.
- Multiple follow‑up questions work within the same session.

NOTES
-----
- yt‑dlp warnings (e.g., missing JS runtime or ffmpeg) are normal and harmless.
- Metadata ingestion does NOT download video or audio streams.
- This script is intended for local testing and debugging of the RAG pipeline.

"""

from app.rag.rag_pipeline import run_rag
from app.ingestion.youtube_ingestion import ingest_video

# from app.db.db import get_transcript_id_for_video, video_has_metadata
from app.ingestion.youtube_metadata_ingestion import ingest_metadata
import uuid  # to generate uniqe session id


def test_full_rag_flow():
    session_id = str(uuid.uuid4())

    print("\n=== FULL RAG PIPELINE TEST ===\n")
    print(f"Session ID: {session_id}")

    # 1 . loop handeling video id and igestion
    while True:
        VIDEO_ID = input("\nEnter YouTube ID (or type 'quit' to exit):").strip()

        if VIDEO_ID.lower() in ("quit", "exit", "kill"):
            print("Exiting test.")
            return

        print("Running ingestion pipelie..\n")
        transcript_id = ingest_video(VIDEO_ID)

        # in case ingestion is succseeded break the loop and continue to RAG
        if transcript_id is not None:
            break

        print(
            "[ERROR] Ingestion failde (e.g., no transcript aailable). Please try another ID"
        )

    # 2. Run RAG with intraction loop, stop by writing quit, exit or kill
    print("# Running RAG pipeline...\n")

    while True:
        query = input("Question: ")
        if query.lower() in ("quit", "exit", "kill"):
            break

        answer = run_rag(query, VIDEO_ID, session_id)

        print(answer)
        print("\n---\n")


if __name__ == "__main__":
    test_full_rag_flow()
