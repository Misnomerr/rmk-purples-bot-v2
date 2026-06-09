def claim_ticket(channel_id, staff_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "ALTER TABLE tickets ADD COLUMN claimed_by INTEGER"
        )
    except:
        pass

    cur.execute(
        """
        UPDATE tickets
        SET claimed_by=?
        WHERE channel_id=?
        """,
        (staff_id, channel_id)
    )

    conn.commit()
    conn.close()


def get_claimed_by(channel_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT claimed_by
            FROM tickets
            WHERE channel_id=?
            """,
            (channel_id,)
        )

        row = cur.fetchone()

        conn.close()

        if row:
            return row[0]

        return None

    except:
        conn.close()
        return None
