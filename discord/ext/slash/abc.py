from typing import Union, Optional, List
import discord
from discord.ext import commands
import aiohttp


class SlashCommand:
    def __init__(self, payload: dict):
        self._payload = payload

    @property
    def id(self):
        return self._payload["id"]

    @property
    def application_id(self):
        return self._payload["application_id"]


class SlashInteraction:
    def __init__(self, payload: dict, session: Optional[aiohttp.ClientSession] = None):
        self._payload = payload
        self._data = self._payload["d"]
        self._session = session

    @property
    def token(self):
        return self._data["token"]

    @property
    def id(self):
        return self._data["id"]

    @property
    def raw_payload(self):
        return self._payload

    @property
    def raw_data(self):
        return self._data

    @property
    def __session__(self):
        return self._session


class SlashContext:
    def __init__(self, bot: Union[discord.Client, commands.Bot], slash_interaction: SlashInteraction):
        self._interaction = slash_interaction
        self._bot = bot
        self.v8 = "https://discord.com/api/v8"
        self.__session__ = self._interaction.__session__

    @property
    def author(self) -> discord.Member:
        _id = self._interaction.raw_data["member"]["user"]["id"]
        return self._bot.get_user(_id)

    @property
    def guild(self) -> discord.Guild or None:
        _id = self._interaction.raw_data["guild_id"]
        return self._bot.get_guild(_id)

    @property
    def channel(self) -> discord.abc.GuildChannel:
        _id = self._interaction.raw_data["channel_id"]
        return self.guild.get_channel(_id)

    async def send(self, content: str, embeds: Optional[List[discord.Embed]] = []):
        application_id = self._interaction.raw_data["application_id"]
        token = self._interaction.token
        route = self.v8 + "/webhooks/{}/{}".format(application_id, token)
        __embeds__ = []
        for embed in embeds:
            __embeds__.append(embed.to_dict())
        json = {
            "content" : content,
            "embeds" : __embeds__
        }
        return await self.__session__.post(route, json = json)

    async def edit(self, content: str, embeds: Optional[List[discord.Embed]] = []):
        application_id = self._interaction.raw_data["application_id"]
        token = self._interaction.token
        route = self.v8 + "/webhooks/{}/{}/messages/@original".format(application_id, token)
        __embeds__ = []
        for embed in embeds:
            __embeds__.append(embed.to_dict())
        json = {
            "content": content,
            "embeds": __embeds__
        }
        return await self.__session__.patch(route, json = json)
