# db update

from datetime import datetime
from app.ingestion.youtube_metadata import fetch_metadata
from app.db.db import update_video_metadata


def ingest_metadata(video_id: str):
    metadata = fetch_metadata(video_id)

    # convert YYYYMMDD to datetime
    published_at = None
    if metadata["published_at"]:
        published_at = datetime.strptime(metadata["published_at"], "%Y%m%d")

        update_video_metadata(
            youtube_id=video_id,
            title=metadata["title"],
            channel=metadata["channel"],
            published_at=published_at,
        )

        return metadata
