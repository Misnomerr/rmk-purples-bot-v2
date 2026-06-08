import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

STAFF_ROLE_ID = int(os.getenv("STAFF_ROLE_ID"))

CREATE_TICKET_CHANNEL_ID = int(
    os.getenv("CREATE_TICKET_CHANNEL_ID")
)

TICKET_LOGS_CHANNEL_ID = int(
    os.getenv("TICKET_LOGS_CHANNEL_ID")
)

FEEDBACK_REVIEW_CHANNEL_ID = int(
    os.getenv("FEEDBACK_REVIEW_CHANNEL_ID")
)

CUSTOMER_FEEDBACK_CHANNEL_ID = int(
    os.getenv("CUSTOMER_FEEDBACK_CHANNEL_ID")
)

TICKETS_CATEGORY_ID = int(
    os.getenv("TICKETS_CATEGORY_ID")
)
