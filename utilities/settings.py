import json
from enum import Enum

path: str
json_file: str


class Key(Enum):
    LOG_CHANNEL = ("log_channel", "Log channel", "Canal où les logs seront envoyés", "🚧", 0)
    MAIN_CHANNEL = ("main_channel", "Main channel", "Canal principal", "💬", 1)


async def read_param(key: Key) -> str:
    params = await read_params()
    return params.get(key.value[0], None)


async def read_params() -> dict[str, str]:
    with open(json_file, "r") as file:
        return json.load(file)


async def write_params(params):
    with open(json_file, "w") as file:
        json.dump(params, file, indent=4)


async def modify_param(key: Key, value: str):
    params = await read_params()
    params[key.value[0]] = value
    await write_params(params)


async def delete_param(key: Key):
    params = await read_params()
    if key in params:
        del params[key.value[0]]
    await write_params(params)


def setup(new_path: str):
    global path, json_file
    path = new_path
    json_file = f"{path}/data/settings.json"
