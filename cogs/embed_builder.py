import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_staff

GUILD_ID = discord.Object(id=1513299075062042777)


class EmbedBuilder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="embedbuilder",
        description="Create a custom embed"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
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
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        embed = discord.Embed(title=title, description=description, color=0x8000ff)
        embed.set_footer(text=footer)
        if image_url:
            embed.set_image(url=image_url)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Embed posted in {channel.mention}", ephemeral=True)

    @app_commands.command(
        name="welcomebuilder",
        description="Create a welcome embed"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def welcomebuilder(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        server_name: str,
        support_channel: discord.TextChannel,
        extra_message: str = None
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        description = (
            f"👋 Welcome to **{server_name}**\n\n"
            f"Thank you for joining our community.\n\n"
            f"🎫 Need support?\n"
            f"Visit {support_channel.mention}\n\n"
            f"📖 Please read our rules and FAQ.\n\n"
            f"We hope you enjoy your stay!"
        )
        if extra_message:
            description += f"\n\n⭐ {extra_message}"

        embed = discord.Embed(title="Welcome", description=description, color=0x8000ff)
        embed.set_footer(text="Welcome to the community")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Welcome embed posted in {channel.mention}", ephemeral=True)

    @app_commands.command(
        name="faqbuilder",
        description="Create a FAQ embed"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def faqbuilder(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        question_1: str,
        answer_1: str,
        question_2: str,
        answer_2: str,
        question_3: str,
        answer_3: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Staff only.", ephemeral=True)
            return

        embed = discord.Embed(title="❓ Frequently Asked Questions", color=0x8000ff)
        embed.add_field(name=question_1, value=answer_1, inline=False)
        embed.add_field(name=question_2, value=answer_2, inline=False)
        embed.add_field(name=question_3, value=answer_3, inline=False)
        embed.set_footer(text="Frequently Asked Questions")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ FAQ posted in {channel.mention}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))
