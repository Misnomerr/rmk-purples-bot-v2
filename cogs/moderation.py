import discord
from discord.ext import commands
from discord import app_commands
import config
from utils.permissions import is_staff
from database import (
    add_blacklisted_word,
    remove_blacklisted_word,
    get_blacklisted_words,
    add_warning,
    get_warnings,
    remove_warning,
    get_warning_count
)
from better_profanity import profanity
from datetime import timedelta

profanity.load_censor_words()

GUILD_ID = discord.Object(id=1513299075062042777)


def check_message(content: str, blacklist: list):

    if profanity.contains_profanity(content):
        return True

    content_lower = content.lower()

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
        name="warn",
        description="Warn a user"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                "❌ Staff only.", ephemeral=True
            )
            return

        warning_id = add_warning(
            member.id,
            interaction.user.id,
            reason
        )

        strike_count = get_warning_count(member.id)

        try:
            await member.send(
                f"⚠️ You have received a warning in **{interaction.guild.name}**.\n\n"
                f"**Reason:** {reason}\n"
                f"**Strike:** {strike_count}/3\n\n"
                f"Please ensure you follow our community rules."
            )
        except discord.HTTPException:
            pass

        if strike_count >= 3:
            try:
                await member.timeout(
                    timedelta(hours=1),
                    reason=f"3 strikes reached. Last reason: {reason}"
                )
            except discord.HTTPException:
                pass

        mod_logs = interaction.guild.get_channel(
            config.MOD_LOGS_CHANNEL_ID
        )

        if mod_logs:

            embed = discord.Embed(
                title="⚠️ User Warned",
                color=0xff8800
            )

            embed.add_field(
                name="User",
                value=f"{member.mention} ({member})",
                inline=False
            )

            embed.add_field(
                name="Reason",
                value=reason,
                inline=False
            )

            embed.add_field(
