import cogs.economy
from utilities import data


async def add_stat(id: int, amount: int, header: data.Header):
    actualStat = int(await data.read_value(id, data.Header.XP))
    newStat = actualStat + amount
    await data.modify_value(id, header, newStat)


async def add_xp(id: int, amount: int):
    await add_stat(id, amount, data.Header.XP)


async def add_money(id: int, amount: int):
    await add_stat(id, amount, data.Header.MONEY)
