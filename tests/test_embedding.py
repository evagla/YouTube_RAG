from app.pipeline import embed_and_store_text

transcript_id = 3  # an exisiting id in db
text = """hela transkriptet här..."""

ids = embed_and_store_text(transcript_id, text)
print(ids)
