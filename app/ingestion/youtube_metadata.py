from yt_dlp import YoutubeDL
from datetime import datetime


# ---------------------------------------------
# Fetch title, channel name and published date
# ----------------------------------------------
def fetch_metadata(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {"skip_download": True, "quiet": True}

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "channel": info.get("channel"),
        "published_at": info.get("upload_date"),
    }


# ---------------------------------------------
# Extract all unique video IDs from a YouTube playlist URL
# ---------------------------------------------


def fetch_playlist_video_ids(playlist_url: str) -> list[str]:
    # clean URL
    if "list=" in playlist_url:
        playlist_id = playlist_url.split("list=")[1].split("&")[0]
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

    print(f"[INFO] Extracting video IDs from playlist: {playlist_url}")

    # setting extract_flat = True to only get the list of IDs
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "extract_flat": True,
        "noplaylist": False,
    }

    video_ids = []

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        # If this is a YouTube playlist, the IDs are in the 'entries', adding the IDs to the list
        if "entries" in info:
            for entry in info["entries"]:
                if entry and "id" in entry:
                    video_ids.append(entry["id"])

    print(f"[INFO] Found {len(video_ids)} videos in playlist")
    return video_ids
