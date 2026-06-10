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
    - If the answer is not found in the context, say: "I cannot find the anser in the video."
    - Do not add external knowledge or assumptions.

    Format:
    Answer: <Your answer>
    Confidence: <0-1>
    """


# -------------------------------
# Run RAG and levels for confidence
# -------------------------------
from typing import List
from app.retrieval.retrieval import retrieve_texts
from app.rag.llm_client import client  # finns ännu inte!!


def llm_confidence_level(value: float) -> str:
    if value is None:
        return "Unkonwn"
    if value < 0.34:
        return "Low"
    elif value < 0.67:
        return "Medium"
    else:
        return "High"


def retrieval_confidence_level(score: float) -> str:
    if score is None:
        return "Unkonwn"
    if score < -5:
        return "Low"
    elif score < -1:
        return "Medium"
    else:
        return "High"


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
    # old:  chunks: List[str] = retrieve_texts(query, youtube_id)
    result = retrieve_texts(query, youtube_id)

    original_query = result["original_query"]
    expanded_query = result["expanded_query"]
    chunks = result["chunks"]
    retrieval_confidence = result["retrieval_confidence"]

    # 2. Build context
    # old: context: str = build_context(chunks)
    context = build_context([row["text"] for row in chunks])

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

    # buil answer with x-tra log info and add info on confidence level
    answer_text = response["message"]["content"].strip()
    llm_confidence = extract_confidence(answer_text)
    level = llm_confidence_level(llm_confidence)
    answer_text = answer_text + f"\nConfidence level: {level}"

    print("\n===== RAG DEBUG PANEL =====")
    print(f"Original query: {original_query}")
    print(f"Expanded query: {expanded_query}")
    print(
        f"Retrieval confidence: {retrieval_confidence} "
        f"({retrieval_confidence_level(retrieval_confidence)})"
    )
    print(f"LLM confidence: {llm_confidence} ({llm_confidence_level(llm_confidence)})")

    """print("\nTop chunks:")
    for row in chunks:
        print(f"- {row['text'][:120]}...")"""

    print("===========================\n")

    # 5. Retruning the answer from Ollama and log info
    return answer_text


def extract_confidence(answer: str) -> float:
    """print("\n--- RAW ANSWER FROM MODEL ---")
    print(answer)
    print("--------- END ANSWER --------\n")"""

    for line in answer.splitlines():
        """ print(f"[CONF-DEBUG] line: {repr(line)}")"""
        if line.lower().startswith("confidence:"):
            try:
                value_str = line.split(":")[1].strip()
                """ print(f"[CONF-DEBUG] found confidence string: {repr(value_str)}")"""
                return float(value_str)
            except Exception as e:
                """print(f"[CONF-DEBUG] failed to parse confidence: {e}")"""
                return None
    """print("[CONF-DEBUG] no confidence line found")"""
    return None
