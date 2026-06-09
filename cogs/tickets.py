import discord
from discord.ext import commands
from discord import app_commands
from views.ticket_panel import CreateTicketButton

GUILD_ID = discord.Object(id=1513299075062042777)


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setup",
        description="Create ticket panel"
    )
    @app_commands.guilds(GUILD_ID)
    async def setup(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="RMK Purples Support",
            description="Click the button below to create a ticket.",
            color=0x8000ff
        )

        await interaction.channel.send(
            embed=embed,
            view=CreateTicketButton()
        )

        await interaction.response.send_message(
            "Ticket panel created.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))
