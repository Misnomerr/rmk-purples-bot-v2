import discord
from discord.ext import commands
from discord import app_commands
from views.feedback_views import FeedbackModal

GUILD_ID = discord.Object(id=1513299075062042777)


class Feedback(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="feedback",
        description="Submit customer feedback"
    )
    @app_commands.guilds(GUILD_ID)
    @app_commands.default_permissions(send_messages=True)
    async def feedback(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            FeedbackModal(self.bot)
        )


async def setup(bot):
    await bot.add_cog(Feedback(bot))
