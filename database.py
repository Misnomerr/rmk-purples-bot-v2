
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
def create_ticket(ticket_number, ticket_type, creator_id, channel_id):
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
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            ticket_number,
            ticket_type,
            creator_id,
            channel_id,
            "open"
        )
    )

    conn.commit()
    conn.close()
