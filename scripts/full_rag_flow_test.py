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
from app.ingestion.youtube_ingestion import ingest_video, ingest_playlist

# from app.db.db import get_transcript_id_for_video, video_has_metadata
from app.ingestion.youtube_metadata_ingestion import ingest_metadata
import uuid  # to generate uniqe session id


def test_full_rag_flow():
    session_id = str(uuid.uuid4())

    print("\n=== FULL RAG PIPELINE TEST ===\n")
    print(f"Session ID: {session_id}")

    VIDEO_ID = None
    PLAYLIST_ID = None

    # 1 . loop handeling video id and igestion
    while True:
        user_input = input(
            "\nEnter YouTube video ID or Playlist URL (or type 'quit' to exit):"
        ).strip()

        if user_input.lower() in ("quit", "exit", "kill"):
            print("Exiting test.")
            return

        # Secenario A: Is it a playlist?
        if "list=" in user_input:
            print(
                "This is not a single video ID. Running playlist ingestion pipeline...\n"
            )
            transcript_ids = ingest_playlist(user_input)

            if transcript_ids:
                print(f"[INFO] Playlist ingestion successfully.")

                if "list=" in user_input:
                    PLAYLIST_ID = user_input.split("list=")[1].split("&")[0]
                print(
                    f"[INFO] Switching to CHAT MODE for the entire playlist: '{PLAYLIST_ID}'"
                )
                break  # break the loop and continue to RAG

                # VIDEO_ID = input(
                #   "\n\nEnter a specific Video ID from the playlist to chat with: "
                # ).strip()
                # break  # break the ingesiton loop and go to RAG
            else:
                print("[ERROR] Playlist ingestion faild or returned no transcripts")
                continue  # start the loop over, asking for a new URL or ID

        # Scenario B: Is it a single video ID?
        else:
            print("Running single video ingestion pipelie...\n")
            transcript_id = ingest_video(user_input)

            # in case ingestion is succseeded break the loop and continue to RAG
            if transcript_id is not None:
                VIDEO_ID = user_input
                break  # break the loop and go to RAG

            print(
                "[ERROR] Ingestion faild (e.g., no transcript aailable). Please try another ID"
            )

    # 2. Run RAG with intraction loop, stop by writing quit, exit or kill
    print(f"\n# Running RAG pipeline agains video '{VIDEO_ID}'...\n")

    while True:
        query = input("Question: ")
        if query.lower() in ("quit", "exit", "kill"):
            break

        answer = run_rag(query, VIDEO_ID, session_id, playlist_id=PLAYLIST_ID)

        print(answer)
        print("\n---\n")


if __name__ == "__main__":
    test_full_rag_flow()
