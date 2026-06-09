import discord
from discord.ext import commands
import os
import asyncio

from database import setup_database
from views.ticket_panel import CreateTicketButton
from views.ticket_controls import TicketControls
from views.feedback_views import FeedbackReviewView

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    bot.add_view(CreateTicketButton())
    bot.add_view(TicketControls())
    bot.add_view(FeedbackReviewView())

    try:

        synced = await bot.tree.sync()

        print(
            f"Synced {len(synced)} commands"
        )

    except Exception as e:

        print(
            f"Sync error: {e}"
        )


async def main():

    setup_database()

    await bot.load_extension(
        "cogs.tickets"
    )

    await bot.load_extension(
        "cogs.feedback"
    )

    await bot.load_extension(
        "cogs.leaderboard"
    )

    await bot.start(
        TOKEN
    )


asyncio.run(main())
