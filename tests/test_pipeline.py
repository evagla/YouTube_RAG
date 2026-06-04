from archive.src.pipeline import embed_and_store_text
from app.db.db import insert_transcript


text = "Det här är ett test. Vi testar embedding och chunking."

transcript_id = insert_transcript(video_id=2, text="dummy")
ids = embed_and_store_text(transcript_id, text)

print(ids)
