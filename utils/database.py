import sqlite3
from datetime import datetime

DB_PATH = "responses.db"


def initialize_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO responses (timestamp, query, response)
    VALUES (?, ?, ?)
    """, (timestamp, query, response))
    conn.commit()
    conn.close()


def get_all_responses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, query, response FROM responses")
    data = cursor.fetchall()
    conn.close()

    return data


def delete_response_by_id(response_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM responses WHERE id = ?", (response_id,))
    conn.commit()
    conn.close()
