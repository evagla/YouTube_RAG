from app.retrieval.retrieval import retrieve_relevant_chunks


def test_retrieval():
    print("Running retrieval")
    results = retrieve_relevant_chunks("what is this video about?", k=5)
    # print("Results: ", results)
    for r in results:
        # print(r[2], r[3][:120])
        print(r["chunk_index"], r["text"][:120])


if __name__ == "__main__":
    test_retrieval()
