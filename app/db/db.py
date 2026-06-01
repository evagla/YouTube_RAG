"""
Database layer
Using Postgres db in Docker
"""

import psycopg2  # PostgreSQL client
from psycopg2.extras import RealDictCursor
import os

1 + 1
# ---------------------------------------
# Database connection
# ---------------------------------------


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="youtube_rag",
        user="raguser",
        password="ragpass",
    )


# ---------------------------------------
# Insert transcript
# ---------------------------------------


def insert_transcript(video_id: str, text: str):
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


# ---------------------------------------
# Insert chunk with embedding
# ---------------------------------------


def insert_chunk(video_id: str, chunk_index: int, text: str, embedding: list):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chunks (video_id, chunk_index, text, embedding)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (video_id, chunk_index, text, embedding),
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
