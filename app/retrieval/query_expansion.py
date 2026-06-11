"""
using query expansion to recieve better answers from model
"""

from app.rag.llm_client import client


def old_expand_query(query: str) -> str:
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


def expand_query(query: str) -> str:
    """
    Expand the user query with a few relevant keywords.
    The original query is always preserved.
    Expansion should be short, stable and retrieval-friendly.
    """

    prompt = f"""
You are helping a retrieval system. Expand the following user query by adding
3–6 relevant keywords or short phrases.

Rules:
- Do NOT rewrite or paraphrase the original question.
- Do NOT remove important words.
- Do NOT change the meaning.
- Only ADD relevant search terms.
- Keep the expansion short (max 12 words).
- Output ONLY the expanded query, nothing else.

Original query: "{query}"
Expanded:
"""

    response = client.chat(
        [
            {
                "role": "system",
                "content": "You expand queries for retrieval. Follow the rules strictly.",
            },
            {"role": "user", "content": prompt},
        ]
    )

    expanded = response["message"]["content"].strip()

    # Combine original + expansion
    return f"{query} {expanded}"
