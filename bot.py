import discord
from discord.ext import commands
import os
import asyncio
from database import setup_database
from views.ticket_panel import CreateTicketButton
from views.ticket_controls import TicketControls
from views.feedback_views import FeedbackReviewView

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = discord.Object(id=1513299075062042777)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.command()
async def sync(ctx):
    if ctx.author.id == 1151788519853924403:
        synced = await bot.tree.sync(guild=GUILD_ID)
        await ctx.send(f"Synced {len(synced)} commands to this server")
    else:
        await ctx.send("❌ No permission.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(CreateTicketButton())
    bot.add_view(TicketControls())
    bot.add_view(FeedbackReviewView())
    print("Ready")

async def main():
    setup_database()
    try:
        await bot.load_extension("cogs.tickets")
        print("✅ Loaded tickets")
    except Exception as e:
        print(f"❌ Tickets error: {e}")
    try:
        await bot.load_extension("cogs.feedback")
        print("✅ Loaded feedback")
    except Exception as e:
        print(f"❌ Feedback error: {e}")
    try:
        await bot.load_extension("cogs.leaderboard")
        print("✅ Loaded leaderboard")
    except Exception as e:
        print(f"❌ Leaderboard error: {e}")
    try:
        await bot.load_extension("cogs.announcements")
        print("✅ Loaded announcements")
    except Exception as e:
        print(f"❌ Announcements error: {e}")
    try:
        await bot.load_extension("cogs.embed_builder")
        print("✅ Loaded embed builder")
    except Exception as e:
        print(f"❌ Embed builder error: {e}")
    await bot.start(TOKEN)

asyncio.run(main())
