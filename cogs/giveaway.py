import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_owner
import asyncio
import random

GUILD_ID = discord.Object(id=1513299075062042777)


class Giveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

        from views.giveaway_view import GiveawayView

        view = GiveawayView()

        embed = discord.Embed(
            title="🎉 Giveaway",
            color=0x8000ff
        )

        embed.add_field(
            name="Prize",
            value=prize,
            inline=False
        )

        embed.add_field(
            name="Winners",
            value=str(winners),
            inline=False
        )

        embed.add_field(
            name="Duration",
            value=duration_text,
            inline=False
        )

        embed.set_footer(
            text="Click the button below to enter!"
        )

        message = await channel.send(
            embed=embed,
            view=view
        )

        await interaction.response.send_message(
            f"✅ Giveaway started in {channel.mention}",
            ephemeral=True
        )

        await asyncio.sleep(seconds)

        view.stop()

        entries = view.entries

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
            value=str(len(entries)),
            inline=False
        )

        if len(entries) == 0:

            ended_embed.add_field(
                name="Winners",
                value="No entries received.",
                inline=False
            )

            ended_embed.set_footer(
                text="Giveaway ended"
            )

            await message.edit(
                embed=ended_embed,
                view=None
            )

        else:

            actual_winners = min(winners, len(entries))

            selected = random.sample(entries, actual_winners)

            winner_mentions = "\n".join(
                [f"<@{uid}>" for uid in selected]
            )

            ended_embed.add_field(
                name=f"Winner{'s' if actual_winners > 1 else ''}",
                value=winner_mentions,
                inline=False
            )

            ended_embed.set_footer(
                text="Giveaway ended"
            )

            await message.edit(
                embed=ended_embed,
                view=None
            )

            await channel.send(
                f"🎉 Congratulations {winner_mentions}! "
                f"You won **{prize}**!"
            )


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
