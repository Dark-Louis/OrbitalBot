import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime

from utilities import bugreport, logs


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report-bug", description="Report un bug")
    async def cmd_bug_report(self, interaction: discord.Interaction):
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/report-bug",
            channel=interaction.channel
        )

        await interaction.response.send_modal(bugreport.ReportBugModal())

    @app_commands.command(name="settings", description="Modifie la valeur d'un paramètre")
    async def cmd_settings(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/settings",
            channel=interaction.channel
        )

        await interaction.followup.send(embed=await bugreport.get_settings_embed(), view=bugreport.SettingsView(interaction))

    @app_commands.command(name="say", description="Envoie un message avec le bot")
    async def cmd_say(self, interaction: discord.Interaction, content: str, channel_id: str = None, reply_message_id: str = None):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/say",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("content", content),
                ("channel_id", channel_id),
                ("reply_message_id", reply_message_id)
            ])
        )

        print(f"Test {channel_id}")
        if channel_id is None:
            channel = interaction.channel
        else:
            channel = await self.bot.fetch_channel(int(channel_id))

        try:
            message_to_reply_to = await interaction.channel.fetch_message(int(reply_message_id))
            await message_to_reply_to.reply(content=content)
        except:
            await channel.send(content=content)

        await interaction.followup.send(content=f"`{content}` **sended in <#{channel.id}>**", ephemeral=True)

    @app_commands.command(name="mp", description="Envoie un message privé avec le bot")
    async def cmd_mp(self, interaction: discord.Interaction, user_id: str, content: str):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/mp",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("user_id", user_id),
                ("content", content)
            ])
        )

        user_id = user_id.replace(" ", "")
        user = await self.bot.fetch_user(int(user_id))
        await user.send(content)

        await interaction.followup.send(content=f"`{content}` **sended to __{user.name}__**", ephemeral=True)

    @app_commands.command(name="userinfo", description="Envoie les informations sur un utilisateur")
    async def cmd_user_info(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await logs.send_log(
            log_type=logs.LogType.COMMAND,
            member=interaction.user,
            name="/userinfo",
            channel=interaction.channel,
            detail=await logs.convert_detail([
                ("user_id", member.id)
            ])
        )

        embed = discord.Embed(
            color=discord.Color.blue(),
            title=f"Information about {member.name}",
            description=f"Here are the details of {member.mention}"
        )

        embed.add_field(name="Username", value=member.name, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=member.status, inline=False)
        embed.add_field(name="Highest role", value=member.top_role, inline=False)

        joined_at = member.joined_at
        joined_at_formatted = datetime.strftime(joined_at, "%d %B %Y %H:%M:%S UTC")
        embed.add_field(name="Joined at", value=joined_at_formatted, inline=False)

        embed.set_thumbnail(url=member.avatar.url)

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Misc(bot))
