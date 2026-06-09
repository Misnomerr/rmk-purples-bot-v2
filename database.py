import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


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
        id SERIAL PRIMARY KEY,
        ticket_number TEXT,
        ticket_type TEXT,
        creator_id BIGINT,
        channel_id BIGINT,
        status TEXT,
        claimed_by BIGINT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        rating INTEGER,
        review TEXT,
        publish_as TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    conn.commit()
    conn.close()


def get_next_ticket_number(category: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT current_number
        FROM ticket_counter
        WHERE category=%s
        """,
        (category,)
    )

    row = cur.fetchone()

    if row:

        number = row[0] + 1

        cur.execute(
            """
            UPDATE ticket_counter
            SET current_number=%s
            WHERE category=%s
            """,
            (number, category)
        )

    else:

        number = 1

        cur.execute(
            """
            INSERT INTO ticket_counter
            (category, current_number)
            VALUES (%s, %s)
            """,
            (category, number)
        )

    conn.commit()
    conn.close()

    return f"{number:04d}"


def create_ticket(
    ticket_number,
    ticket_type,
    creator_id,
    channel_id
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tickets
        (
            ticket_number,
            ticket_type,
            creator_id,
            channel_id,
            status,
            claimed_by
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            ticket_number,
            ticket_type,
            creator_id,
            channel_id,
            "open",
            None
        )
    )

    conn.commit()
    conn.close()


def claim_ticket(channel_id, staff_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tickets
        SET claimed_by=%s
        WHERE channel_id=%s
        """,
        (
            staff_id,
            channel_id
        )
    )

    conn.commit()
    conn.close()


def get_claimed_by(channel_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT claimed_by
        FROM tickets
        WHERE channel_id=%s
        """,
        (channel_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None
