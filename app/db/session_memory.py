import uuid
import psycopg2


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


def load_history(conn, session_id, limit=5):
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
