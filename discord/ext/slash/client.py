import discord
from discord.ext import commands
from typing import Union, Optional, List
from slash.gateway import Gateway
from slash.abc import SlashInteraction, SlashContext
import asyncio
import json

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
            payload_data = payload["d"]
            slash_id = payload_data["data"]["id"]
            interaction_id = payload_data["id"]
            interaction_token = payload_data["token"]
            command_key = self._slash_commands.get(slash_id)
            if command_key is not None:
                ack = await self._gateway.ack_heartbeat(int(interaction_id), interaction_token)
                print(await ack.text())
                inter_slash = SlashInteraction(payload, self._session)
                context = SlashContext(self._bot, inter_slash)
                func = command_key.get("func")
                coro = func
                await coro(context)
            
                


    def slash_command(self, name : str, description : str, options : Optional[List[dict]] = [], guild_ids : Optional[List[int]] = []):
        
        def wrapper(func):
            loop = asyncio.get_event_loop()
            if len(guild_ids) != 0:
                for guild_id in guild_ids:
                    slash_command = loop.run_until_complete(self._gateway.create_command(name, description, options = options, guild_id = guild_id))
                    self._slash_commands.update({slash_command.id : {"cmd" : slash_command, "func" : func}})
                    print("Created slashy")
            else:
                slash_command = loop.run_until_complete(self._gateway.create_command(name, description, options = options))
                self._slash_commands.update({slash_command.id : {"cmd" : slash_command, "func" : func}})
                print("Created slashy")

            print(self._slash_commands)


            
            

        return wrapper
            