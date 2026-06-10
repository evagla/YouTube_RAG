"""
Reranking retrievals using bge‑reranker‑base
"outof this 15 chunks, which 5 are the most relevant ones"
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load once at import
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-base")
model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-base")


def rerank(query: str, rows: list, top_k: int = 5):
    """
    rows : list of dicts form DB, each containing "text"
    returns: top_k rows sorted by relevance
    """

    print("Reranking...")
    pairs = [(query, row["text"]) for row in rows]

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512,
    )

    with torch.no_grad():
        scores = model(**inputs).logits.squeeze()

    # Sort rows by score, desc
    scored_rows = list(zip(scores.tolist(), rows))
    scored_rows.sort(key=lambda x: x[0], reverse=True)

    for score, row in scored_rows:
        row["score"] = score

    # DEBUG LOGGING
    print("\n === RERANKER SCORES===")
    for score, row in scored_rows:
        print(f"Score: {score: 4f} | Text: {row['text'][:80]}...")
    print("=========================")

    # Only return rows and score
    return [row for score, row in scored_rows[:top_k]]

    # print out score
    best_score = scored_rows[0][0]
    print(f"Reranker confidence (best score): {best_score: .4f}")
