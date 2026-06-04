"""
Retrieval -> Prompt -> Answer from LLM

user question - get relevant chunks - build context - build RAG-prompt - send prompt to LLM - return answer to user question
"""

from typing import List

# -------------------------------
# Building context from chunks
# -------------------------------


def build_context(chunks: List[str]) -> str:
    cleaned = [c.strip().replace("\n", " ") for c in chunks]
    context = "\n\n".join(cleaned)
    return context


# -------------------------------
# Building RAG-prompt for the model to only give replies based on the transcript content
# -------------------------------


def build_prompt(query: str, context: str) -> str:
    """
    Builds a clean and reliable RAG prompt in English.
    The model is instructed to answer strictly based on the provided context.

    """
    return f"""
    You are an assistant that answers questions based strictly on the contet of a YouTube video.

    Here is the relevant context extracted from the video:
    ---
    {context}
    ---

    User question:
    {query}

    Instructions:
    - Answer ONLY using the information n the context above.
    - If the answer isnot found in the context, say: "I cannot find the anser in the video."
    - Do not add external knowledge or assumptions.
    """


# -------------------------------
# Run RAG
# -------------------------------
from typing import List
from app.retrieval.retrieval import retrieve_texts
from app.rag.llm_client import client  # finns ännu inte!!


def run_rag(query: str, youtube_id: str) -> str:
    """
    Run the whole RAG-pipeline:
    1.Fetching relevant chunks by using retrieval
    2.Building context
    3.Building promt
    4.Sending prompt to LLM
    5.Returning the answer
    """

    # 1. Retrieval
    chunks: List[str] = retrieve_texts(query, youtube_id)

    # 2. Build context
    context: str = build_context(chunks)

    # 3. Build prompt
    prompt: str = build_prompt(query, context)

    # 4. Send promt to LLM using roles
    response = client.chat(
        [
            {
                "role": "system",
                "content": "You answer strictly based on the provided context.",
            },
            {"role": "user", "content": prompt},
        ]
    )

    # 5. Retruning the answer from Ollama
    return response["message"]["content"].strip()
