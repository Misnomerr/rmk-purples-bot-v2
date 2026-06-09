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

        try:

            guild = interaction.guild

            ticket_type = self.values[0]

            number = get_next_ticket_number(ticket_type)

            channel_name = f"{ticket_type}-{number}"

            category = guild.get_channel(
                config.TICKETS_CATEGORY_ID
            )

            if category is None:
                await interaction.response.send_message(
                    "❌ Tickets category not found.",
                    ephemeral=True
                )
                return

            staff_role = guild.get_role(
                config.STAFF_ROLE_ID
            )

            if staff_role is None:
                await interaction.response.send_message(
                    "❌ Staff role not found.",
                    ephemeral=True
                )
                return

            bot_member = guild.get_member(
                interaction.client.user.id
            )

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),

                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                ),

                staff_role: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                ),

                bot_member: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                )
            }

            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )

            create_ticket(
                number,
                ticket_type,
                interaction.user.id,
                channel.id
            )

            embed = discord.Embed(
                title="Ticket Created",
                description=(
                    f"Type: {ticket_type}\n"
                    f"Ticket: {channel_name}"
                ),
                color=0x8000ff
            )

            await channel.send(
                f"{interaction.user.mention}"
            )

            await channel.send(embed=embed)

            await interaction.response.send_message(
                f"✅ Created {channel.mention}",
                ephemeral=True
            )

        except Exception as e:

            print(f"TICKET ERROR: {e}")

            await interaction.response.send_message(
                f"❌ Error: {e}",
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
