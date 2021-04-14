import discord
from discord.ext import commands
from typing import Union, Optional, List
from slash.gateway import Gateway
from slash.abc import SlashInteraction


class SlashBot:
    def __init__(self, bot : Union[discord.Client, commands.Bot]):
        self._bot = bot
        self._token = self._bot.http.token
        self._id = None
        self._gateway = Gateway(self._id, self._token, self._bot)
        self._bot.on_socket_response = self.on_socket_response
        self._slash_commands = {}
        self._pending_interactions = {}
        self._session = self._gateway.session


    async def on_socket_response(self, payload):
        print(payload)
        payload = dict(payload) #safety is our no1 priority (its a joke)
        if payload["t"] == "READY":
            self._id = self._bot.user.id
        if payload["t"] == "INTERACTION_CREATE":
            data = payload["d"]
            token = data["token"]
            interaction_id = int(data["id"])
            slash_interaction = SlashInteraction(payload)
            print("=====DEBUG DATA=====")
            print(slash_interaction.token)
            print(slash_interaction.raw_data["application_id"])
            response = await self._gateway.ack_heartbeat(interaction_id, token)
            self._pending_interactions.update({interaction_id : slash_interaction})
            key = self._slash_commands.get(interaction_id)
            if key is not None:
                func = key["func"]
                


    def slash_command(self, name : str, description : str, options : Optional[List[dict]] = []):
        pass
        
            