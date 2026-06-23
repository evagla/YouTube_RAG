from sentence_transformers import SentenceTransformer
from config.config import load_settings


settings = load_settings()
emb_config = settings.get("embeddings", {})

# get parpmeters dynamically and define defaults
model_name = emb_config.get("model", "all-MiniLM-L6-v2")
device = emb_config.get("device", "cpu")


# init transformer model
model = SentenceTransformer(model_name, device=device)
print(f"Embedding model '{model_name}' is running on {device}")


def embed_text(text: str):
    embedding = model.encode(text)
    return embedding.tolist()
