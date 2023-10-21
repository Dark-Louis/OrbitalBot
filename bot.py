import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

from datetime import datetime

from utilities import data, logs, settings, member_stats

# path = "/home/louis/AtlasBot"
path = "D:/Programmes/Python/OrbitalBot"
load_dotenv(dotenv_path=f"{path}/config")

bot: commands.bot.Bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
guild: discord.Guild


@bot.event
async def on_ready():
    global guild

    await bot.load_extension("cogs.economy")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.misc")

    guild = await bot.fetch_guild(1141334556906102896)
    data.setup(guild, path)
    logs.setup(bot)
    settings.setup(path)

    play_status = discord.Game(name="être codé")
    await bot.change_presence(status=discord.Status.online, activity=play_status)

    print("The bot is now functional.")

    try:
        synced = await bot.tree.sync()
        print("The bot is now synchronized with " + str(len(synced)) + " commands:")
        for cmd in synced:
            print("- " + cmd.name)
    except Exception as e:
        print("The bot is not synchronized: " + str(e))


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await member_stats.add_xp(message.author.id, 1)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot:
        return

    await logs.send_log(
        log_type=logs.LogType.MODIFIED_MESSAGE,
        member=before.author,
        name="Modified message",
        detail=f"**__Before__**\n{before.content}\n\n**__After__**\n{after.content}",
        link=after.jump_url
    )


@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return

    await logs.send_log(
        log_type=logs.LogType.DELETED_MESSAGE,
        member=message.author,
        name="Deleted message",
        detail=f"**__Before__**\n{message.content}",
        link=message.jump_url
    )


@bot.event
async def on_member_join(member: discord.Member):
    await logs.send_log(
        log_type=logs.LogType.MEMBER_JOIN,
        member=member,
        name="New member"
    )

    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")

    await data.modify_value(member.id, data.Header.JOIN_DATE, formatted_date)


@bot.event
async def on_member_remove(member: discord.Member):
    await logs.send_log(
        log_type=logs.LogType.MEMBER_LEAVE,
        member=member,
        name="Member left"
    )
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")

    await data.modify_value(member.id, data.Header.LEAVE_DATE, formatted_date)


if os.getenv("TOKEN") == "ENTER YOUR TOKEN":
    print("Enter your token in the config file, just after the \"TOKEN=\"")
    print("Don't forget to modify the \"path\" at the top of the script, line 12")
else:
    bot.run(os.getenv("TOKEN"))
