from app.rag.rag_pipeline import run_rag


def test():
    question = "which plants are recomended and, shortly why?"
    answer = run_rag(question)
    print("\n=== RAG ANSWER ===\n")
    print(answer)
    print("\n===================\n")


if __name__ == "__main__":
    test()
