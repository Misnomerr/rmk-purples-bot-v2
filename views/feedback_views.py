import discord
import config

from utils.permissions import is_owner

from database import (
    increment_feedback_approved
)


class FeedbackReviewView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Approve",
        emoji="✅",
        style=discord.ButtonStyle.success,
        custom_id="approve_feedback"
    )
    async def approve_feedback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_owner(interaction.user):

            await interaction.response.send_message(
                "❌ Owners only.",
                ephemeral=True
            )
            return

        embed = interaction.message.embeds[0]

        rating = embed.fields[0].value
        review = embed.fields[1].value
        publish_as = embed.fields[3].value

        customer_channel = (
            interaction.guild.get_channel(
                config.CUSTOMER_FEEDBACK_CHANNEL_ID
            )
        )

        if customer_channel is None:

            await interaction.response.send_message(
                "❌ Customer feedback channel not found.",
                ephemeral=True
            )
            return

        public_embed = discord.Embed(
            title="Customer Feedback",
            color=0x8000ff
        )

        public_embed.add_field(
            name="Rating",
            value=rating,
            inline=False
        )

        public_embed.add_field(
            name="Review",
            value=review,
            inline=False
        )

        public_embed.set_footer(
            text=f"Submitted By: {publish_as}"
        )

        await customer_channel.send(
            embed=public_embed
        )

        increment_feedback_approved(
            interaction.user.id
        )

        approved_embed = embed.copy()

        approved_embed.color = 0x00ff00

        approved_embed.add_field(
            name="Status",
            value=(
                f"✅ Approved by "
                f"{interaction.user.mention}"
            ),
            inline=False
        )

        await interaction.message.edit(
            embed=approved_embed,
            view=None
        )

        await interaction.response.send_message(
            "✅ Feedback approved.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Reject",
        emoji="❌",
        style=discord.ButtonStyle.danger,
        custom_id="reject_feedback"
    )
    async def reject_feedback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not is_owner(interaction.user):

            await interaction.response.send_message(
                "❌ Owners only.",
                ephemeral=True
            )
            return

        embed = interaction.message.embeds[0]

        rejected_embed = embed.copy()

        rejected_embed.color = 0xff0000

        rejected_embed.add_field(
            name="Status",
            value=(
                f"❌ Rejected by "
                f"{interaction.user.mention}"
            ),
            inline=False
        )

        await interaction.message.edit(
            embed=rejected_embed,
            view=None
        )

        await interaction.response.send_message(
            "❌ Feedback rejected.",
            ephemeral=True
        )


class FeedbackModal(discord.ui.Modal, title="Submit Feedback"):

    def __init__(self, bot):
        super().__init__()

        self.bot = bot

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
        label="Anonymous? (Y/N)",
        placeholder="Y or N",
        max_length=3
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        try:

            rating_number = int(
                self.rating.value
            )

            if rating_number < 1 or rating_number > 5:

                await interaction.response.send_message(
                    "❌ Rating must be between 1 and 5.",
                    ephemeral=True
                )
                return

            stars = "⭐" * rating_number

            anonymous = (
                self.anonymous.value
                .strip()
                .lower()
                in ["y", "yes"]
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
                    "Anonymous Customer"
                    if anonymous
                    else interaction.user.display_name
                ),
                inline=False
            )

            await review_channel.send(
                embed=embed,
                view=FeedbackReviewView()
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
