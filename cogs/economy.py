import discord
from discord.ext import commands
from discord import app_commands

from utilities import data, logs


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Enregistre l'utilisateur dans la base de données")
    async def cmd_register(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/register",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("member", member.id)
            ])
        )

        if member.bot:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is a bot.**")
            return

        if not await data.is_existing(member.id):
            await data.register(member.id)
            await interaction.followup.send(content=f"**✅ __{member.name}__ has been registered in the database.**")
        else:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is already registered in the database.**")

    @app_commands.command(name="unregister", description="Enlève l'utilisateur de la base de données")
    async def cmd_unregister(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/unregister",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("member", member.id)
            ])
        )

        if member.bot:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is a bot.**")
            return

        if await data.is_existing(member.id):
            await data.unregister(member.id)
            await interaction.followup.send(content=f"**✅ __{member.name}__ was removed from the database.**")
        else:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is not saved in the database.**")

    @app_commands.command(name="get", description="Obtient les données de l'utilisateur")
    async def cmd_get(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/get",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("member", member.id)
            ])
        )

        if member.bot:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is a bot.**")
            return

        headers = []
        for header in data.Header:
            headers.append(header.name.lower())
        headers = ",".join(headers)

        line = await data.read_line(member.id)
        line = ",".join(line)

        message = f"**Here is the data from {member.name} :**\n```{headers}\n{line}```"

        await interaction.followup.send(content=message)

    @app_commands.command(name="modify", description="Obtient les données de l'utilisateur")
    @app_commands.choices(key=[app_commands.Choice(name=header.name.lower(), value=header.value) for header in data.Header])
    async def cmd_modify(self, interaction: discord.Interaction, member: discord.Member, key: app_commands.Choice[int], value: str):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/modify",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("member", member.id),
                ("key", list(data.Header)[key.value].name),
                ("value", value)
            ])
        )

        if member.bot:
            await interaction.followup.send(content=f"**❌ __{member.name}__ is a bot.**")
            return

        old_value = await data.read_value(member.id, list(data.Header)[key.value])

        if old_value == value:
            await interaction.followup.send(content=f"**The data is the same.**")

        await data.modify_value(member.id, list(data.Header)[key.value], value)

        await interaction.followup.send(content=f"**Here is the new data for __{member.name}__:**\n```diff\n- {key.name} = {old_value}``````diff\n+ {key.name} = {value}```")


async def setup(bot):
    await bot.add_cog(Economy(bot))
