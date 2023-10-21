import discord

from enum import Enum


class Type(Enum):
    Member = discord.member.Member
    User = discord.user.User
    UserId = int


async def convert_type(type_input: discord.Member | discord.user.User | int, type_output: Type) -> discord.member.Member | discord.user.User | int:
    if type_output.value == discord.member.Member:
        if type(type_input) == discord.user.User:
            return await guild.fetch_member(type_input.id)
        elif type(type_input) == int:
            return await guild.fetch_member(type_input)
    elif type_output.value == discord.user.User:
        if type(type_input) == discord.member.Member:
            return await bot.fetch_user(type_input.id)
        elif type(type_input) == int:
            return await bot.fetch_user(type_input)
    else:
        return type_input.id
