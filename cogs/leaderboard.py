import discord
from discord.ext import commands
from discord import app_commands
from database import get_staff_stats, get_leaderboard
from utils.permissions import is_staff

GUILD_ID = discord.Object(id=1513299075062042777)


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="mystats",
        description="View your staff statistics"
    )
    @app_commands.guilds(GUILD_ID)
    async def mystats(self, interaction: discord.Interaction):

        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        stats = get_staff_stats(interaction.user.id)

        embed = discord.Embed(
            title=f"📊 {interaction.user.display_name}",
            color=0x8000ff
        )
        embed.add_field(name="Tickets Claimed", value=stats["tickets_claimed"], inline=False)
        embed.add_field(name="Tickets Closed", value=stats["tickets_closed"], inline=False)
        embed.add_field(name="Feedback Approved", value=stats["feedback_approved"], inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="staffstats",
        description="View staff statistics"
    )
    @app_commands.guilds(GUILD_ID)
    async def staffstats(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        stats = get_staff_stats(member.id)

        embed = discord.Embed(
            title=f"📊 {member.display_name}",
            color=0x8000ff
        )
        embed.add_field(name="Tickets Claimed", value=stats["tickets_claimed"], inline=False)
        embed.add_field(name="Tickets Closed", value=stats["tickets_closed"], inline=False)
        embed.add_field(name="Feedback Approved", value=stats["feedback_approved"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="leaderboard",
        description="View staff leaderboard"
    )
    @app_commands.guilds(GUILD_ID)
    async def leaderboard(self, interaction: discord.Interaction):

        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        leaderboard = get_leaderboard()

        embed = discord.Embed(
            title="🏆 Staff Leaderboard",
            color=0x8000ff
        )

        if not leaderboard:
            embed.description = "No staff statistics found."
        else:
            lines = []
            for position, row in enumerate(leaderboard, start=1):
                member = interaction.guild.get_member(row[0])
                if member:
                    total = row[1] + row[2] + row[3]
                    lines.append(
                        f"**{position}. {member.display_name}**\n"
                        f"Claims: {row[1]} | Closed: {row[2]} | "
                        f"Approved: {row[3]} | Score: {total}"
                    )
            embed.description = "\n\n".join(lines)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
