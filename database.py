# ADD THESE FUNCTIONS AT THE BOTTOM OF database.py


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
