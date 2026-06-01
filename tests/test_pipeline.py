from app.services.pipeline import embed_and_store_text

text = "Det här är ett test. Vi testar embedding och chunking."
ids = embed_and_store_text("test_video_123", text)

print(ids)
