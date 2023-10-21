import discord
from discord.ext import commands
from enum import Enum

from utilities import settings

bot: commands.bot.Bot


class LogType(Enum):
    COMMAND = (0x5a00a0, "https://cdn-icons-png.flaticon.com/512/1628/1628954.png")
    MODIFIED_MESSAGE = (0xffc800, "https://cdn-icons-png.flaticon.com/512/1827/1827933.png")
    DELETED_MESSAGE = (0xffa000, "https://cdn-icons-png.flaticon.com/512/11580/11580308.png")
    MEMBER_JOIN = (0x00ff00, "https://cdn-icons-png.flaticon.com/512/716/716570.png")
    MEMBER_LEAVE = (0xff0000, "https://cdn-icons-png.flaticon.com/512/716/716571.png")


async def send_log(log_type: LogType, member: discord.Member, name: str, channel: discord.TextChannel | discord.VoiceChannel = None, detail: str = None, link: str = None):
    if link:
        embed = discord.Embed(
            title=name,
            url=link,
            color=log_type.value[0]
        )
    else:
        embed = discord.Embed(
            title=name,
            color=log_type.value[0]
        )

    embed.set_author(name=f"@{member.name} - {member.id}", icon_url=member.avatar.url)
    embed.set_thumbnail(url=log_type.value[1])

    if detail:
        embed.add_field(name=" ", value=detail)

    if channel:
        embed.set_footer(text=f"#{channel.name} - {channel.id}")

    log_channel = await bot.fetch_channel(int(await settings.read_param(settings.Key.LOG_CHANNEL)))
    await log_channel.send(embed=embed)


async def convert_detail(details: list[tuple[str, str | int]]) -> str:
    output = ""
    for name, value in details:
        output += f"{name}: `{value}`\n"
        return output.strip()


def setup(new_bot: commands.bot.Bot):
    global bot
    bot = new_bot
