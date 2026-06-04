"""
Database layer
Using Postgres db in Docker
"""

import psycopg2  # PostgreSQL client
from psycopg2.extras import RealDictCursor
import os
from pgvector.psycopg2 import register_vector
import time
from typing import List, Dict, Any

# ---------------------------------------
# SQL Search constant
# ---------------------------------------
SQL_SEARCH_CHUNKS = """
SELECT id, transcript_id, chunk_index, text, embedding,
    (embedding <-> (%s)::vector) AS distence
FROM chunks
ORDER BY embedding <-> (%s)::vector
LIMIT %s;
"""


# ---------------------------------------
# Database connection
# ---------------------------------------


def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="youtube_rag",
        user="raguser",
        password="ragpass",
    )
    register_vector(conn)
    return conn


# ---------------------------------------
# Insert video
# ---------------------------------------


def insert_video(
    youtube_id: str, title: str = None, channel: str = None, published_at=None
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO videos (youtube_id, title, channel, published_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (youtube_id, title, channel, published_at),
    )

    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


# ---------------------------------------
# Insert transcript
# ---------------------------------------


def insert_transcript(video_id: int, text: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO transcripts (video_id, text)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (video_id, text),
    )

    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


'''
# ---------------------------------------
# Insert chunk with embedding
# ---------------------------------------


def insert_chunk(transcript_id: str, chunk_index: int, text: str, embedding: list):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chunks (transcript_id, chunk_index, text, embedding)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (transcript_id, chunk_index, text, embedding),
    )

    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

'''
# ---------------------------------------
# Insert chunk (without embedding)
# ---------------------------------------


def insert_chunk(transcript_id: int, chunk_index: int, text: str, embedding=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chunks (transcript_id, chunk_index, text, embedding)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (transcript_id, chunk_index, text, embedding),
    )

    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


# ---------------------------------------
# Fetch chunks for a video
# ---------------------------------------


def get_chunks_by_video(video_id: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT id, chunk_index, text, embedding
        FROM chunks
        WHERE video_id = %s
        ORDER BY chunk_index ASC;
        """,
        (video_id,),
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ---------------------------------------
# Search using pgvectorscale
# ---------------------------------------
"""
-  <-> = cosine distance in pgvector
-  the lowest value = the closest
-  returning top-k chunks

"""


def search_chunks(query_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
    k = min(k, 20)  # do not use a lager k value than 20

    with get_connection() as conn:
        # with conn.cursor() as cur:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            start = time.time()

            '''cur.execute(
                """
                SELECT id, transcript_id, chunk_index, text, embedding, (embedding <-> (%s)::vector) AS distance
                FROM chunks
                ORDER BY embedding <-> (%s)::vector
                LIMIT %s;
                """,
                (query_embedding, query_embedding, k),
            )'''

            cur.execute(
                SQL_SEARCH_CHUNKS, (query_embedding, query_embedding, k)
            )  # use the sql search constant

            # return cur.fetchall()
            rows = cur.fetchall()
            duration = time.time() - start
            print(
                f"search_chunks: returned: {len(rows)} rows in {duration:.4f} seconds"
            )
            if not rows:
                return []
            return rows


# ---------------------------------------
# Get chunks from db - to test embedding
# ---------------------------------------
def get_chunks_for_transcript(transcript_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, text
                FROM chunks
                WHERE transcript_id = %s
                ORDER BY id;
                """,
                (transcript_id,),
            )
            return cur.fetchall()


# ---------------------------------------
# update the embedding column
# ---------------------------------------
def update_chunk_embedding(chunk_id: int, embedding):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE chunks
                SET embedding = %s
                WHERE id = %s;
                """,
                (embedding, chunk_id),
            )
            conn.commit()


# ---------------------------------------
# get db transkript_id for a youtoube video
# ---------------------------------------
def get_transcript_id_for_video(youtube_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT t.id
        FROM transcripts t
        JOIN videos v On v.id = t.video_id
        WHERE v.youtube_id = %s
        """,
        (youtube_id,),
    )

    row = cur.fetchall()
    cur.close()
    conn.close()
    return row[0] if row else None


# ---------------------------------------
# Search using pgvectorscale in chunks for a specified video
# ---------------------------------------


def search_chunks_for_transcript(transcript_id: int, query_embedding, k: int = 5):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, transcript_id, chunk_index, text, embedding, (embedding <-> (%s)::vector) AS distance
                FROM chunks
                WHERE transcript_id = %s
                ORDER BY embedding <-> (%s)::vector
                LIMIT %s;
                """,
                (query_embedding, transcript_id, query_embedding, k),
            )
            return cur.fetchall()
