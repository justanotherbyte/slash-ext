import discord
from discord.ext import commands
from typing import Union, Optional, List
from slash.gateway import Gateway
from slash.abc import SlashInteraction
import asyncio


class SlashBot:
    def __init__(self, bot : Union[discord.Client, commands.Bot], bot_token : str, bot_id : int):
        self._bot = bot
        self._token = self._bot.http.token or bot_token
        print(self._token)
        self._id = bot_id
        self._gateway = Gateway(self._id, self._token, self._bot)
        self._bot.on_socket_response = self.on_socket_response
        self._slash_commands = {}
        self._pending_interactions = {}
        self._session = self._gateway.session


    async def on_socket_response(self, payload):
        payload = dict(payload) #safety is our no1 priority (its a joke)
        if payload["t"] == "READY":
            self._id = self._bot.user.id
        if payload["t"] == "INTERACTION_CREATE":
            data = payload["d"]
            token = data["token"]
            interaction_id = int(data["id"])
            slash_interaction = SlashInteraction(payload)
            response = await self._gateway.ack_heartbeat(interaction_id, token)
            self._pending_interactions.update({interaction_id : slash_interaction})
            key = self._slash_commands.get(interaction_id)
            if key is not None:
                func = key["func"]
                


    def slash_command(self, name : str, description : str, options : Optional[List[dict]] = [], guild_ids : Optional[List[int]] = []):
        
        def wrapper(func):
            loop = asyncio.get_event_loop()
            if len(guild_ids) != 0:
                for guild_id in guild_ids:
                    slash_command = loop.run_until_complete(self._gateway.create_command(name, description, options = options, guild_id = guild_id))
                    self._slash_commands.update({slash_command.id : slash_command})
                    print("Created slashy")
            else:
                slash_command = loop.run_until_complete(self._gateway.create_command(name, description, options = options))
                self._slash_commands.update({slash_command.id : slash_command})
                print("Created slashy")

            print(self._slash_commands)


            
            

        return wrapper
            