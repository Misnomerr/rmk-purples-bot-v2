import discord
import asyncio
import config

from io import BytesIO

from utils.transcripts import generate_transcript


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
