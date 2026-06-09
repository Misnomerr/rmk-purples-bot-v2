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

async def load(extension, name):
    try:
        await bot.load_extension(extension)
        print(f"✅ Loaded {name}")
    except commands.ExtensionAlreadyLoaded:
        await bot.reload_extension(extension)
        print(f"🔄 Reloaded {name}")
    except Exception as e:
        print(f"❌ {name} error: {e}")

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
    await load("cogs.tickets", "tickets")
    await load("cogs.feedback", "feedback")
    await load("cogs.leaderboard", "leaderboard")
    await load("cogs.announcements", "announcements")
    await load("cogs.embed_builder", "embed builder")
    await bot.start(TOKEN)

asyncio.run(main())
