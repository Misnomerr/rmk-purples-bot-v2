import discord
from discord.ext import commands
from discord import app_commands
import config
from utils.permissions import is_staff
from database import (
    add_blacklisted_word,
    remove_blacklisted_word,
    get_blacklisted_words
)

GUILD_ID = discord.Object(id=1513299075062042777)

BUILT_IN_FILTER = [
    "nigger", "nigga", "faggot", "fag", "chink",
    "spic", "kike", "tranny", "retard", "cunt",
    "gook", "wetback", "beaner", "cracker", "dyke",
    "paki", "raghead", "sandnigger", "zipperhead",
    "coon", "jigaboo", "spook", "towelhead", "wop",
    "dago", "greaseball", "heeb", "hymie", "kyke",
    "shylock", "slope", "slant"
]


def check_message(content: str, blacklist: list):

    content_lower = content.lower()

    for word in BUILT_IN_FILTER:
        if word in content_lower:
            return True

    for word in blacklist:
        if word.lower() in content_lower:
            return True

    return False


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        blacklist = get_blacklisted_words()

        if not check_message(message.content, blacklist):
            return

        try:
            await message.delete()
        except discord.HTTPException:
            pass

        try:
            await message.author.send(
                f"⚠️ Your message in **{message.guild.name}** was removed "
                f"as it contained language that violates our community standards. "
                f"Please review our rules."
            )
        except discord.HTTPException:
            pass

        mod_logs = message.guild.get_channel(
            config.MOD_LOGS_CHANNEL_ID
        )

        if mod_logs:

            embed = discord.Embed(
                title="⚠️ Message Filtered",
                color=0xff0000
            )

            embed.add_field(
                name="User",
                value=f"{message.author.mention} ({message.author})",
                inline=False
            )

            embed.add_field(
                name="Channel",
                value=message.channel.mention,
                inline=False
            )

            embed.add_field(
                name="Message",
                value=message.content[:1024],
                inline=False
            )

            await mod_logs.send(embed=embed)

    @app_commands.command(
        name="addword",
        description="Add a word to the blacklist"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def addword(
        self,
        interaction: discord.Interaction,
        word: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Staff only.", ephemeral=True
            )
            return

        add_blacklisted_word(word)

        await interaction.response.send_message(
            f"✅ **{word}** has been added to the blacklist.",
            ephemeral=True
        )

    @app_commands.command(
        name="removeword",
        description="Remove a word from the blacklist"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def removeword(
        self,
        interaction: discord.Interaction,
        word: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Staff only.", ephemeral=True
            )
            return

        remove_blacklisted_word(word)

        await interaction.response.send_message(
            f"✅ **{word}** has been removed from the blacklist.",
            ephemeral=True
        )

    @app_commands.command(
        name="listwords",
        description="View the current blacklist"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def listwords(
        self,
        interaction: discord.Interaction
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Staff only.", ephemeral=True
            )
            return

        words = get_blacklisted_words()

        if not words:
            await interaction.response.send_message(
                "📋 The blacklist is currently empty.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📋 Custom Blacklist",
            description="\n".join(words),
            color=0x8000ff
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
