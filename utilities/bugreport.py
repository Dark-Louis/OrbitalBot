import discord

from utilities import settings


class SettingsView(discord.ui.View):
    def __init__(self, old_interaction: discord.Interaction):
        super().__init__()
        self.old_interaction = old_interaction

    @discord.ui.select(
        placeholder="Select a parameter to modify...",
        options=[discord.SelectOption(label=key.value[1], description=key.value[2], emoji=key.value[3], value=key.value[4]) for key in settings.Key]
    )
    async def select_setting(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        value = await settings.read_param(list(settings.Key)[int(select_item.values[0])])
        await interaction.response.send_modal(SettingsModal(int(select_item.values[0]), value, self.old_interaction))


class SettingsModal(discord.ui.Modal):
    def __init__(self, index: int, value: str, old_interaction: discord.Interaction, title="Changing a setting"):
        super().__init__(title=title)
        self.key = list(settings.Key)[index]
        self.value = value
        self.old_interaction = old_interaction

        self.new_value = discord.ui.TextInput(
            label=f"Currently, {self.key.value[0]} = {self.value}",
            placeholder=f"New value for {self.key.value[0]}...",
            style=discord.TextStyle.short
        )
        self.add_item(self.new_value)

    async def on_submit(self, interaction: discord.Interaction):
        await settings.modify_param(self.key, str(self.new_value))
        await interaction.response.send_message(content=f"**Here is the new data for __{self.key.value[0]}__:**\n```diff\n- {self.key.value[0]} = {self.value}``````diff\n+ {self.key.value[0]} = {self.new_value}```")
        message = await self.old_interaction.original_response()
        await message.edit(embed=await get_settings_embed())


async def get_settings_embed() -> discord.Embed:
    parameters = await settings.read_params()
    embed = discord.Embed(
        title="Bot settings",
        description="_ _"
    )

    for key, value in parameters.items():
        embed.add_field(
            name=key,
            value=value,
            inline=False
        )

    return embed


class ReportBugModal(discord.ui.Modal):
    def __init__(self, title="Bug report"):
        super().__init__(title=title)
        self.channel = discord.ui.TextInput(
            label="In which channel did the bug occur?",
            placeholder="#General...",
            style=discord.TextStyle.short
        )
        self.add_item(self.channel)

        self.command = discord.ui.TextInput(
            label="Which command did the bug occur with?",
            placeholder="/help...",
            style=discord.TextStyle.short
        )
        self.add_item(self.command)

        self.detail = discord.ui.TextInput(
            label="Describe the bug you encountered",
            placeholder="There was a red message...",
            style=discord.TextStyle.long
        )
        self.add_item(self.detail)

    async def on_submit(self, interaction: discord.Interaction):
        darklouis59 = await guild.fetch_member(1088406477204623440)
        await darklouis59.send(f"**{interaction.user}** - {interaction.user.id}\n`{self.command}` in `{self.channel}`\n{self.detail}")
        await interaction.response.send_message(content="**Report sent!**\nThanks \\:)", ephemeral=True, delete_after=5)
