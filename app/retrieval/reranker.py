"""
Reranking retrievals using bge‑reranker‑base
"outof this 15 chunks, which 5 are the most relevant ones"
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from config.config import load_settings

settings = load_settings()
rerank_config = settings.get("reranker", {})

# Pull parameters dynamically with fallback values
model_name = rerank_config.get("model", "BAAI/bge-reranker-base")
max_length = rerank_config.get("max_length", 512)
default_top_k = rerank_config.get("top_k", 5)
device = rerank_config.get("device", "cpu")

# Load once at import
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
print(f"Reranker model '{model_name}' is running on: {device.upper()}")


def rerank(query: str, rows: list, top_k: int = None):
    """
    rows : list of dicts form DB, each containing "text"
    returns: top_k rows sorted by relevance
    """

    # Fall back
    if top_k is None:
        top_k = default_top_k

    print("...Reranking...")
    pairs = [(query, row["text"]) for row in rows]

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=max_length,
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        # Handle cases where rows has only 1 item ot prevent squeeze() from breaking dimensions
        if len(rows) == 1:
            scores = logits.squeeze(-1)
        else:
            scores = logits.squeeze()

    # Convert tensor scores based on structure
    if len(rows) == 1:
        scores_list = [scores.item()]
    else:
        scores_list = scores.tolist()

    # Sort rows by score, desc
    scored_rows = list(zip(scores_list, rows))
    scored_rows.sort(key=lambda x: x[0], reverse=True)

    for score, row in scored_rows:
        row["score"] = score

    # DEBUG LOGGING
    """print("\n === RERANKER SCORES===")
    for score, row in scored_rows:
        print(f"Score: {score: 4f} | Text: {row['text'][:80]}...")
    print("=========================")"""

    # print out score
    if scored_rows:
        best_score = scored_rows[0][0]
        print(f"Reranker confidence (best score): {best_score: .4f}")

    # Only return rows and score
    return [row for score, row in scored_rows[:top_k]]
