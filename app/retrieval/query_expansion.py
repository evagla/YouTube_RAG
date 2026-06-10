"""
using query expansion to recieve better answers from model
"""

from app.rag.llm_client import client


def expand_query(query: str) -> str:
    """
    Rewrite the query in a clearer way for retrieval.
    Keep it short, factual, and do NOT add new information.
    """

    response = client.chat(
        [
            {
                "role": "system",
                "content": (
                    "Your task is NOT to answer the question. Your ONLY task is to rewrite the user query for search retrieval."
                    "Rewrite it as a short, direct search query."
                    "Do NOT ask for more information. "
                    "Do NOT answer the question. "
                    "Do NOT explain anything."
                    "Do NOT add details. "
                    " Output ONLY the rewritten query."
                ),
            },
            {"role": "user", "content": query},
        ],
        temperature=0.0,
    )

    return response["message"]["content"].strip()
