import discord

from discord.ext import commands
from discord import app_commands

from utils.permissions import is_staff


class EmbedBuilder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="embedbuilder",
        description="Create a custom embed"
    )
    async def embedbuilder(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        description: str,
        footer: str,
        image_url: str = None
    ):

        if not is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ Staff only.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=0x8000ff
        )

        embed.set_footer(
            text=footer
        )

        if image_url:

            embed.set_image(
                url=image_url
            )

        await channel.send(
            embed=embed
        )

        await interaction.response.send_message(
            f"✅ Embed posted in {channel.mention}",
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        EmbedBuilder(bot)
    )
