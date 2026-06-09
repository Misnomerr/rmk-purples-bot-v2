import discord
import asyncio


class TicketControls(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Claim",
        emoji="📌",
        style=discord.ButtonStyle.primary,
        custom_id="claim_ticket"
    )
    async def claim_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            f"📌 Claimed by {interaction.user.mention}",
            ephemeral=False
        )

    @discord.ui.button(
        label="Close",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🔒 Closing ticket in 5 seconds..."
        )

        await asyncio.sleep(5)

        await interaction.channel.delete()
