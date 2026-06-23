import uuid
import psycopg2
from config.config import load_settings

settings = load_settings()
session_config = settings.get("session_memory", {})

DEFAULT_MAX_TURNS = session_config.get("max_turns", 5)


def save_interaction(conn, session_id, user_message, assistant_message):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO sessions (session_id, user_message, assistant_message)
            VALUES (%s, %s, %s)
            """,
            (session_id, user_message, assistant_message),
        )
    conn.commit()


def load_history(conn, session_id, limit=None):
    # Fall back if needed
    if limit is None:
        limit = DEFAULT_MAX_TURNS

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT user_message, assistant_message
            FROM sessions
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (session_id, limit),
        )
        rows = cur.fetchall()

    return list(reversed(rows) if rows else [])
