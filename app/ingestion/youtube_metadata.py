import yt_dlp
from datetime import datetime
# from app.ingestion


# ---------------------------------------------
# Fetch title, channel name and published date
# ----------------------------------------------
def fetch_metadata(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {"skip_download": True, "quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "channel": info.get("channel"),
        "published_at": info.get("upload_date"),
    }
