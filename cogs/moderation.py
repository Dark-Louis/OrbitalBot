import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime

from utilities import logs


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Supprime les messages d'un utilisateur dans un channel")
    async def cmd_delete(self, interaction: discord.Interaction, amount: int, user_id: str = None):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/purge",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("amount", amount),
                ("user_id", user_id)
            ])
        )

        if amount > 100:
            amount = 100

        channel = interaction.channel
        messages = []
        async for message in channel.history():
            if user_id is not None:
                user_id = user_id.replace(" ", "")
                if message.author.id == int(user_id):
                    messages.append(message)
                    if len(messages) == amount:
                        break
            elif message != await interaction.original_response():
                messages.append(message)
                if len(messages) == amount:
                    break

        await channel.delete_messages(messages)
        await interaction.followup.send(content=f"**{amount} messages from <#{channel.id}> have been deleted.**")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
