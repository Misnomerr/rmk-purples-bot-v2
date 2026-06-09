import discord

from discord.ext import commands
from discord import app_commands

from database import (
    get_staff_stats,
    get_leaderboard
)


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="staffstats",
        description="View staff statistics"
    )
    async def staffstats(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        stats = get_staff_stats(
            member.id
        )

        embed = discord.Embed(
            title=f"📊 {member.display_name}",
            color=0x8000ff
        )

        embed.add_field(
            name="Tickets Claimed",
            value=stats["tickets_claimed"],
            inline=False
        )

        embed.add_field(
            name="Tickets Closed",
            value=stats["tickets_closed"],
            inline=False
        )

        embed.add_field(
            name="Feedback Approved",
            value=stats["feedback_approved"],
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="leaderboard",
        description="View staff leaderboard"
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction
    ):

        leaderboard = get_leaderboard()

        embed = discord.Embed(
            title="🏆 Staff Leaderboard",
            color=0x8000ff
        )

        if not leaderboard:

            embed.description = (
                "No staff statistics found."
            )

        else:

            lines = []

            for position, row in enumerate(
                leaderboard,
                start=1
            ):

                member = (
                    interaction.guild.get_member(
                        row[0]
                    )
                )

                if member:

                    total = (
                        row[1]
                        + row[2]
                        + row[3]
                    )

                    lines.append(
                        f"**{position}. "
                        f"{member.display_name}**\n"
                        f"Claims: {row[1]} | "
                        f"Closed: {row[2]} | "
                        f"Approved: {row[3]} | "
                        f"Score: {total}"
                    )

            embed.description = "\n\n".join(
                lines
            )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Leaderboard(bot)
    )
