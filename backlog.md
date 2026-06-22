# BACKLOG
This backlog outlines the planned improvements for the project.
The list is intentionally short and focused to keep the repository clear and approachable.

- [ ] 1. **Centralize configuration in settings.yaml**\
Unify all configuration (LLM, embeddings, reranker, chunking, retrieval, database, cache) into a single file to simplify setup and experimentation.

2. **Improve ingestion pipeline**\
Enhance ingestion with playlist support, skip‑existing behavior, better error handling, and clearer logging.

3. **Configurable embeddings and reranker**\
Move model selection to settings.yaml and support multiple embedding and reranker models without code changes.

4. **Support multiple LLM providers**\
Add a provider‑agnostic LLM layer supporting Ollama (default), OpenAI, Azure OpenAI, and HuggingFace.

5. **Multiple chunking strategies**\
Introduce configurable chunking methods (fixed, sentence‑based, simple semantic) to improve retrieval quality.

6. **Multiple retrieval strategies**\
Add support for dense, BM25, and hybrid retrieval to increase robustness and accuracy.

7. **Caching layer**\
Implement caching for transcripts, embeddings, retrieval results, and LLM responses to improve performance.

8. **Basic evaluation framework**\
Add a small evaluation set and simple metrics (recall@k, MRR, basic RAG evaluation) to measure system quality over time.
