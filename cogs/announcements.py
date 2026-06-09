import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_staff

GUILD_ID = discord.Object(id=1513299075062042777)


class Announcements(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="announce",
        description="Post an announcement"
    )
    @app_commands.guilds(GUILD_ID)
    async def announce(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        embed = discord.Embed(title="📢 Announcement", description=message, color=0x8000ff)
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Announcement posted in {channel.mention}", ephemeral=True)

    @app_commands.command(
        name="embedannounce",
        description="Post an embedded announcement"
    )
    @app_commands.guilds(GUILD_ID)
    async def embedannounce(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        message: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        embed = discord.Embed(title=f"📢 {title}", description=message, color=0x8000ff)
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Announcement posted in {channel.mention}", ephemeral=True)

    @app_commands.command(
        name="poll",
        description="Create a poll"
    )
    @app_commands.guilds(GUILD_ID)
    async def poll(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        question: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        embed = discord.Embed(title="📊 Community Poll", description=question, color=0x8000ff)
        embed.set_footer(text=f"Created by {interaction.user.display_name}")
        poll_message = await channel.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")
        await interaction.response.send_message(f"✅ Poll created in {channel.mention}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Announcements(bot))
