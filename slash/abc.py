from typing import Union
import discord
from discord.ext import commands

class SlashContext():
    def __init__(self, response_payload : dict, bot : Union[discord.Client, commands.Bot] = None):
        self._payload = response_payload
        self._bot = bot or None

    @property
    def command_id(self) -> int:
        return self._payload.get("id")


    @property
    def raw_payload(self) -> dict:
        return self._payload

    """@property
    def guild(self) -> discord.Guild or None:
        if "guild_id" in self._payload:
            return self._bot.get_guild(self._payload["guild_id"])
        else:
            return None"""
    


class SlashCommand:
    def __init__(self, create_payload : dict):
        self._payload = create_payload
        self._data = self._payload["d"]

    @property
    def id(self):
        return self._data["id"]

