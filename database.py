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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff_stats (
        staff_id BIGINT PRIMARY KEY,
        tickets_claimed INTEGER DEFAULT 0,
        tickets_closed INTEGER DEFAULT 0,
        feedback_approved INTEGER DEFAULT 0
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

    cur.execute(
        """
        INSERT INTO staff_stats
        (
            staff_id,
            tickets_claimed
        )
        VALUES (%s, 1)
        ON CONFLICT (staff_id)
        DO UPDATE SET
        tickets_claimed =
        staff_stats.tickets_claimed + 1
        """,
        (staff_id,)
    )

    conn.commit()
    conn.close()


def increment_closed(staff_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO staff_stats
        (
            staff_id,
            tickets_closed
        )
        VALUES (%s, 1)
        ON CONFLICT (staff_id)
        DO UPDATE SET
        tickets_closed =
        staff_stats.tickets_closed + 1
        """,
        (staff_id,)
    )

    conn.commit()
    conn.close()


def increment_feedback_approved(staff_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO staff_stats
        (
            staff_id,
            feedback_approved
        )
        VALUES (%s, 1)
        ON CONFLICT (staff_id)
        DO UPDATE SET
        feedback_approved =
        staff_stats.feedback_approved + 1
        """,
        (staff_id,)
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


def get_staff_stats(staff_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            tickets_claimed,
            tickets_closed,
            feedback_approved
        FROM staff_stats
        WHERE staff_id=%s
        """,
        (staff_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:

        return {
            "tickets_claimed": row[0],
            "tickets_closed": row[1],
            "feedback_approved": row[2]
        }

    return {
        "tickets_claimed": 0,
        "tickets_closed": 0,
        "feedback_approved": 0
    }


def get_leaderboard():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            staff_id,
            tickets_claimed,
            tickets_closed,
            feedback_approved
        FROM staff_stats
        ORDER BY
            (
                tickets_claimed +
                tickets_closed +
                feedback_approved
            ) DESC
        LIMIT 10
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows
