import discord
from database import (
    add_giveaway_entry,
    get_giveaway_entry_count,
    get_giveaway_by_message
)


class GiveawayView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Enter Giveaway (0)",
        emoji="🎉",
        style=discord.ButtonStyle.primary,
        custom_id="enter_giveaway"
    )
    async def enter_giveaway(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        giveaway = get_giveaway_by_message(interaction.message.id)

        if not giveaway:
            await interaction.response.send_message(
                "❌ This giveaway could not be found.",
                ephemeral=True
            )
            return

        giveaway_id = giveaway[0]
        status = giveaway[5]

        if status != "active":
            await interaction.response.send_message(
                "❌ This giveaway has already ended.",
                ephemeral=True
            )
            return

        entered = add_giveaway_entry(giveaway_id, interaction.user.id)

        if not entered:
            await interaction.response.send_message(
                "❌ You have already entered this giveaway.",
                ephemeral=True
            )
            return

        count = get_giveaway_entry_count(giveaway_id)

        button.label = f"Enter Giveaway ({count})"

        await interaction.message.edit(view=self)

        await interaction.response.send_message(
            "✅ You have entered the giveaway. Good luck!",
            ephemeral=True
        )
