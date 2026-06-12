YouTube RAG — Retrieval‑Augmented Generation on YouTube Transcripts.
This repository contains a complete Retrieval‑Augmented Generation (RAG) pipeline built around YouTube videos.
The system ingests metadata and transcripts, chunks text, generates embeddings, stores vectors in PostgreSQL + pgvector, retrieves relevant chunks, reranks them, and produces final answers using an LLM.

The project is designed to be modular, configurable, and easy to extend.

# Features
YouTube metadata ingestion (yt-dlp)

YouTube transcript ingestion (youtube-transcript-api)

Text chunking with configurable size & overlap

Embeddings via sentence-transformers

Vector storage in PostgreSQL + pgvector

Vector similarity search

Query expansion (improves recall)

Reranking using BAAI/bge-reranker-base

Session memory (per‑session conversation context)

LLM integration (e.g., Ollama running llama3.2:latest)

Fully configurable via config/settings.yaml

End‑to‑end test: full_rag_flow_test.py

# Prerequisites
To run this project locally, you need:

System
Python 3.10+

Git

Database
PostgreSQL 15+

pgvector extension installed:

sql
CREATE EXTENSION IF NOT EXISTS vector;
LLM Runtime
If using Ollama:

bash
ollama pull llama3.2
Optional
Docker (if you want to run Postgres via container)

GPU (for faster embeddings / reranking)

# Installation
1. Clone the repository
bash
git clone <repo-url>
cd <repo>
2. Create a virtual environment
bash
python -m venv .venv
source .venv/bin/activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Start PostgreSQL + pgvector
If using Docker:

bash
docker-compose up -d

# Configuration (config/settings.yaml)
All pipeline settings are controlled through:

LLM configuration

Embedding model

Chunking parameters

Retrieval parameters

Reranker model

Database connection

Debug options

Example:

yaml
llm:
  model: "llama3.2:latest"
  provider: "ollama"
  url: "http://localhost:11434/api/chat"

# Project Structure
Code
app/
  ingestion/
    youtube_metadata.py
    youtube_transcript.py
  processing/
    chunking.py
    embeddings.py
  retrieval/
    retrieval.py
    reranker.py
  rag/
    rag_pipeline.py
    query_expansion.py
  db/
    db.py
    session_memory.py
config/
  settings.yaml
tests/
  full_rag_flow_test.py
  test_rag_pipeline.py
  test_retrieval.py
  test_embedding.py
  test_full_pipeline.py
requirements.txt
README.md
BACKLOG.md

# Running the Pipeline
The recommended way to run the full RAG pipeline is via the included end‑to‑end test:

bash
python tests/full_rag_flow_test.py

This script:

asks for a YouTube video ID

ingests metadata and transcript (if not already in DB)

runs the full RAG loop

allows interactive questioning

maintains session memory

This is the correct way to run the system in its current state.

# Tests
Run all tests:

bash
pytest
Run the full end‑to‑end test:

bash
python tests/full_rag_flow_test.py

# Architecture Diagrams
A) High‑Level Overview
mermaid
flowchart LR
    A[YouTube Video] --> B[Ingestion]
    B --> C[Chunking]
    C --> D[Embeddings]
    D --> E[(Postgres + pgvector)]
    F[User Query] --> G[Query Expansion]
    G --> H[Retrieval]
    H --> I[Reranker]
    I --> J[LLM]
    J --> K[Final Answer]
    
B) Detailed Pipeline
mermaid
flowchart TD
    subgraph Ingestion
        A1[yt-dlp metadata]
        A2[youtube-transcript-api]
    end

    subgraph Processing
        B1[Chunking]
        B2[SentenceTransformers Embeddings]
    end

    subgraph Database
        C1[(Postgres)]
        C2[(pgvector)]
    end

    subgraph Retrieval
        D1[Query Expansion]
        D2[Vector Search]
        D3[BGE Reranker]
    end

    subgraph Generation
        E1[LLM Client]
        E2[Session Memory]
    end

    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> C2
    C2 --> D2
    D2 --> D3
    D3 --> E1
    E1 --> E2
    E2 --> F[Final Answer]
