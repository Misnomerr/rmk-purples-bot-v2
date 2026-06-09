import discord
from io import StringIO


async def generate_transcript(channel: discord.TextChannel):

    transcript = StringIO()

    transcript.write(
        f"Transcript for #{channel.name}\n"
    )

    transcript.write(
        "=" * 50 + "\n\n"
    )

    async for message in channel.history(
        limit=None,
        oldest_first=True
    ):

        timestamp = message.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        transcript.write(
            f"[{timestamp}] "
            f"{message.author}: "
            f"{message.content}\n"
        )

        if message.attachments:

            for attachment in message.attachments:

                transcript.write(
                    f"ATTACHMENT: "
                    f"{attachment.url}\n"
                )

        transcript.write("\n")

    transcript.seek(0)

    return transcript
