import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ticket_counter (
        category TEXT PRIMARY KEY,
        current_number INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT,
        ticket_type TEXT,
        creator_id INTEGER,
        channel_id INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_next_ticket_number(category: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT current_number FROM ticket_counter WHERE category=?",
        (category,)
    )

    row = cur.fetchone()

    if row:
        number = row[0] + 1
        cur.execute(
            "UPDATE ticket_counter SET current_number=? WHERE category=?",
            (number, category)
        )
    else:
        number = 1
        cur.execute(
            "INSERT INTO ticket_counter(category,current_number) VALUES(?,?)",
            (category, number)
        )

    conn.commit()
    conn.close()

    return f"{number:04d}"
