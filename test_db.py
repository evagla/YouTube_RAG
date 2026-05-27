from src.db import get_connection

try:
    conn = get_connection()
    print("Connected:", conn)
    conn.close()
except Exception as e:
    print("Error:", e)

1 + 1
