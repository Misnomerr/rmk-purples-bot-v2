import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_owner
from views.giveaway_view import GiveawayView
from database import (
    create_giveaway,
    get_giveaway_entries,
    get_active_giveaways,
    end_giveaway_db,
    get_giveaway_entry_count
)
import asyncio
import random
from datetime import datetime, timedelta

GUILD_ID = discord.Object(id=1513299075062042777)


async def run_giveaway(bot, giveaway_id, message_id, channel_id, prize, winners, end_time):

    now = datetime.utcnow()
    remaining = (end_time - now).total_seconds()

    if remaining > 0:
        await asyncio.sleep(remaining)

    guild = None
    for g in bot.guilds:
        guild = g
        break

    if not guild:
        return

    channel = guild.get_channel(channel_id)

    if not channel:
        return

    try:
        message = await channel.fetch_message(message_id)
    except discord.HTTPException:
        return

    entries = get_giveaway_entries(giveaway_id)
    count = len(entries)

    end_giveaway_db(giveaway_id)

    ended_embed = discord.Embed(
        title="🎉 Giveaway Ended",
        color=0x8000ff
    )

    ended_embed.add_field(
        name="Prize",
        value=prize,
        inline=False
    )

    ended_embed.add_field(
        name="Entries",
        value=str(count),
        inline=False
    )

    if count == 0:

        ended_embed.add_field(
            name="Winners",
            value="No entries received.",
            inline=False
        )

        ended_embed.set_footer(text="Giveaway ended")

        await message.edit(embed=ended_embed, view=None)

    else:

        actual_winners = min(winners, count)
        selected = random.sample(entries, actual_winners)
        winner_mentions = "\n".join([f"<@{uid}>" for uid in selected])

        ended_embed.add_field(
            name=f"Winner{'s' if actual_winners > 1 else ''}",
            value=winner_mentions,
            inline=False
        )

        ended_embed.set_footer(text="Giveaway ended")

        await message.edit(embed=ended_embed, view=None)

        await channel.send(
            f"🎉 Congratulations {winner_mentions}! "
            f"You won **{prize}**!"
        )


class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        active = get_active_giveaways()

        for row in active:
            giveaway_id, message_id, channel_id, prize, winners, end_time = row
            asyncio.create_task(
                run_giveaway(
                    self.bot,
                    giveaway_id,
                    message_id,
                    channel_id,
                    prize,
                    winners,
                    end_time
                )
            )

        print(f"🎉 Resumed {len(active)} active giveaway(s)")

    @app_commands.command(
        name="giveaway",
        description="Start a giveaway"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    @app_commands.describe(
        duration_unit="minutes, hours, or days"
    )
    async def giveaway(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        prize: str,
        winners: int,
        duration: int,
        duration_unit: str
    ):
        if not is_owner(interaction.user):
            await interaction.response.send_message(
                "❌ Owners only.",
                ephemeral=True
            )
            return

        duration_unit = duration_unit.lower()

        if duration_unit not in ["minutes", "hours", "days"]:
            await interaction.response.send_message(
                "❌ Duration unit must be minutes, hours, or days.",
                ephemeral=True
            )
            return

        if duration_unit == "minutes":
            seconds = duration * 60
            duration_text = f"{duration} minute{'s' if duration != 1 else ''}"
        elif duration_unit == "hours":
            seconds = duration * 3600
            duration_text = f"{duration} hour{'s' if duration != 1 else ''}"
        else:
            seconds = duration * 86400
            duration_text = f"{duration} day{'s' if duration != 1 else ''}"

        end_time = datetime.utcnow() + timedelta(seconds=seconds)

        view = GiveawayView()

        embed = discord.Embed(
            title="🎉 Giveaway",
            color=0x8000ff
        )

        embed.add_field(name="Prize", value=prize, inline=False)
        embed.add_field(name="Winners", value=str(winners), inline=False)
        embed.add_field(name="Duration", value=duration_text, inline=False)
        embed.set_footer(text="Click the button below to enter!")

        message = await channel.send(embed=embed, view=view)

        giveaway_id = create_giveaway(
            message.id,
            channel.id,
            prize,
            winners,
            end_time
        )

        await interaction.response.send_message(
            f"✅ Giveaway started in {channel.mention}",
            ephemeral=True
        )

        asyncio.create_task(
            run_giveaway(
                self.bot,
                giveaway_id,
                message.id,
                channel.id,
                prize,
                winners,
                end_time
            )
        )


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
