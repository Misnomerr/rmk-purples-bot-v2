import discord


class GiveawayView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.entries = []

    @discord.ui.button(
        label="Enter Giveaway",
        emoji="🎉",
        style=discord.ButtonStyle.primary,
        custom_id="enter_giveaway"
    )
    async def enter_giveaway(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id in self.entries:

            await interaction.response.send_message(
                "❌ You have already entered this giveaway.",
                ephemeral=True
            )
            return

        self.entries.append(interaction.user.id)

        await interaction.response.send_message(
            "✅ You have entered the giveaway. Good luck!",
            ephemeral=True
        )
