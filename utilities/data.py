import discord

import csv
from enum import Enum

guild: discord.Guild

path: str
csv_file: str


class Header(Enum):
    ID = 0
    NAME = 1
    MONEY = 2
    XP = 3
    JOIN_DATE = 4
    LEAVE_DATE = 5


async def read_line(id: int | str) -> list:
    if not await is_existing(id):
        await register(id)

    with open(file=csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)

        for line in reader:
            if line[0] == str(id):
                return line


async def read_value(id: int | str, key: Header) -> str:
    line = await read_line(id)
    return line[key.value]


async def write_line(id: int | str, name: str, money: int | str, xp: int | str, join_date: str, leave_date: str):
    if await is_existing(id):
        return

    with open(file=csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        lines = []
        for line in reader:
            lines.append(line)

    with open(file=csv_file, mode="w", encoding="utf-8", newline="") as ff:
        writer = csv.writer(ff)
        writer.writerows(lines)
        writer.writerow([id, name, money, xp, join_date, leave_date])


async def modify_value(id: int | str, key: Header, value: any):
    if not await is_existing(id):
        await register(id)

    with open(file=csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        lines = []
        for line in reader:
            if line[0] == str(id):
                line[key.value] = str(value)
            lines.append(line)

    with open(file=csv_file, mode="w", encoding="utf-8", newline="") as ff:
        writer = csv.writer(ff)
        writer.writerows(lines)


async def unregister(id: int):
    with open(file=csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        lines = []
        for line in reader:
            if line[0] == str(id):
                continue
            lines.append(line)

    with open(file=csv_file, mode="w", encoding="utf-8", newline="") as ff:
        writer = csv.writer(ff)
        writer.writerows(lines)


async def register(id: int):
    if await is_existing(id):
        return

    member = await guild.fetch_member(id)
    await write_line(id, member.name, 0, 0, "---", "---")


async def is_existing(id: int | str) -> bool:
    with open(file=csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)

        for line in reader:
            if line[0] == str(id):
                return True

    return False


def setup(new_guild: discord.Guild, new_path: str):
    global guild, path, csv_file
    guild = new_guild
    path = new_path
    csv_file = f"{path}/data/data.csv"

