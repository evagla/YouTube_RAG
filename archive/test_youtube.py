from src.youtube import fetch_transcript

video_id = "hXlSicZE9jI"  # byt till valfri video
text = fetch_transcript(video_id)

print(text[:500])  # skriv ut första 500 tecken


1 + 1
