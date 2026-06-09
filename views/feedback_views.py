import discord
import config


class FeedbackModal(discord.ui.Modal, title="Submit Feedback"):

    rating = discord.ui.TextInput(
        label="Rating (1-5)",
        placeholder="Enter a number between 1 and 5",
        max_length=1
    )

    review = discord.ui.TextInput(
        label="Review",
        style=discord.TextStyle.paragraph,
        placeholder="Tell us about your experience",
        max_length=1000
    )

    anonymous = discord.ui.TextInput(
        label="Anonymous? (Yes/No)",
        placeholder="Yes or No",
        max_length=3
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        try:

            rating_number = int(self.rating.value)

            if rating_number < 1 or rating_number > 5:

                await interaction.response.send_message(
                    "❌ Rating must be between 1 and 5.",
                    ephemeral=True
                )
                return

            stars = "⭐" * rating_number

            anonymous = (
                self.anonymous.value.strip().lower()
                == "yes"
            )

            review_channel = (
                interaction.guild.get_channel(
                    config.FEEDBACK_REVIEW_CHANNEL_ID
                )
            )

            if review_channel is None:

                await interaction.response.send_message(
                    "❌ Review channel not found.",
                    ephemeral=True
                )
                return

            embed = discord.Embed(
                title="New Feedback Submission",
                color=0x8000ff
            )

            embed.add_field(
                name="Rating",
                value=stars,
                inline=False
            )

            embed.add_field(
                name="Review",
                value=self.review.value,
                inline=False
            )

            embed.add_field(
                name="Submitted By",
                value=interaction.user.mention,
                inline=False
            )

            embed.add_field(
                name="Publish As",
                value=(
                    "Anonymous"
                    if anonymous
                    else interaction.user.display_name
                ),
                inline=False
            )

            await review_channel.send(
                embed=embed
            )

            await interaction.response.send_message(
                "✅ Feedback submitted for review.",
                ephemeral=True
            )

        except ValueError:

            await interaction.response.send_message(
                "❌ Rating must be a number between 1 and 5.",
                ephemeral=True
            )
