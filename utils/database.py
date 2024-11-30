import sqlite3
from datetime import datetime

DB_PATH = "responses.db"


def connect_to_db():
    return sqlite3.connect(DB_PATH)


def initialize_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def save_response_to_db(query, response):
    conn = connect_to_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO responses (timestamp, query, response)
    VALUES (?, ?, ?)
    """, (timestamp, query, response))
    conn.commit()
    conn.close()


def get_all_responses():
    conn = connect_to_db()
    cursor = conn.cursor()

    if not table_exists("responses"):
        initialize_db()

    cursor.execute("SELECT id, timestamp, query, response FROM responses")
    data = cursor.fetchall()
    conn.close()

    return data


def delete_response_by_id(response_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM responses WHERE id = ?", (response_id,))
    conn.commit()
    is_deleted = cursor.rowcount > 0
    conn.close()

    return is_deleted


def table_exists(table_name: str) -> bool:
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (table_name,))
    result = cursor.fetchone()
    conn.close()

    return result is not None
