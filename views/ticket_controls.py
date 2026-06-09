import discord
import asyncio
import config

from io import BytesIO

from utils.transcripts import generate_transcript

from database import (
    claim_ticket,
    get_claimed_by
)


class TicketControls(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Claim",
        emoji="📌",
        style=discord.ButtonStyle.primary,
        custom_id="claim_ticket"
    )
    async def claim_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        staff_role = interaction.guild.get_role(
            config.STAFF_ROLE_ID
        )

        if staff_role not in interaction.user.roles:

            await interaction.response.send_message(
                "❌ Staff only.",
                ephemeral=True
            )
            return

        claimed_by = get_claimed_by(
            interaction.channel.id
        )

        if claimed_by:

            member = interaction.guild.get_member(
                claimed_by
            )

            if member:

                await interaction.response.send_message(
                    f"❌ Already claimed by {member.mention}",
                    ephemeral=True
                )

            else:

                await interaction.response.send_message(
                    "❌ Ticket already claimed.",
                    ephemeral=True
                )

            return

        claim_ticket(
            interaction.channel.id,
            interaction.user.id
        )

        embed = discord.Embed(
            title="📌 Ticket Claimed",
            description=(
                f"{interaction.user.mention} "
                f"has claimed this ticket."
            ),
            color=0x8000ff
        )

        await interaction.response.send_message(
            embed=embed
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
            "🔒 Generating transcript..."
        )

        transcript = await generate_transcript(
            interaction.channel
        )

        transcript_file = discord.File(
            BytesIO(
                transcript.getvalue().encode("utf-8")
            ),
            filename=f"{interaction.channel.name}.txt"
        )

        logs_channel = interaction.guild.get_channel(
            config.TICKET_LOGS_CHANNEL_ID
        )

        if logs_channel:

            embed = discord.Embed(
                title="Ticket Closed",
                color=0x8000ff
            )

            embed.add_field(
                name="Channel",
                value=interaction.channel.name,
                inline=False
            )

            embed.add_field(
                name="Closed By",
                value=interaction.user.mention,
                inline=False
            )

            await logs_channel.send(
                embed=embed,
                file=transcript_file
            )

        await interaction.followup.send(
            "🔒 Ticket closing in 5 seconds..."
        )

        await asyncio.sleep(5)

        await interaction.channel.delete()
