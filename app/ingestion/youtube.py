# Frist version, only fetching transkript ( no metadata)

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


def fetch_transcript(video_id: str) -> str:
    """
    Fetch the transcript for a YouTube video and return it
    as a single text string.
    """

    try:
        api = YouTubeTranscriptApi()

        # Try Swedish first, then English
        try:
            entries = api.fetch(video_id, languages=["sv"])
        except:
            entries = api.fetch(video_id, languages=["en"])

    except TranscriptsDisabled:
        raise Exception(f"Transcripts are disabled for video {video_id}")
    except NoTranscriptFound:
        raise Exception(f"No transcript found for video {video_id}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching transcript: {e}")

    # entries är en lista av FetchedTranscriptSnippet-objekt
    full_text = " ".join(snippet.text for snippet in entries)

    return full_text
