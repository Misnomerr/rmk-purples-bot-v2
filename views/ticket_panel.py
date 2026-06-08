import discord
import config

from database import (
    get_next_ticket_number,
    create_ticket
)

class TicketTypeSelect(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="Chambers of Xeric",
                emoji="⚔️",
                value="cox"
            ),
            discord.SelectOption(
                label="Payments",
                emoji="💰",
                value="payments"
            ),
            discord.SelectOption(
                label="Other",
                emoji="❓",
                value="other"
            )
        ]

        super().__init__(
            placeholder="Choose a ticket type...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"You selected: {self.values[0]}",
            ephemeral=True
        )


class TicketTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

        self.add_item(TicketTypeSelect())


class CreateTicketButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        emoji="🎫",
        style=discord.ButtonStyle.blurple,
        custom_id="create_ticket"
    )
    async def create_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "Select a ticket type:",
            view=TicketTypeView(),
            ephemeral=True
        )
