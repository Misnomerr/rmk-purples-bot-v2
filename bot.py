import discord
from discord.ext import commands
import os
import asyncio

from database import setup_database

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

async def main():
    setup_database()

    await bot.load_extension("cogs.tickets")

    synced = await bot.tree.sync()

    print(f"Synced {len(synced)} commands")

    await bot.start(TOKEN)

asyncio.run(main())
