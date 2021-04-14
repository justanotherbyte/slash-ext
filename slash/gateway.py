import aiohttp
import asyncio
from typing import Optional, Union
from slash.abc import SlashContext
import discord
from discord.ext import commands








class Gateway:
    def __init__(self, application_id : int, token : str, bot : Union[discord.Client, commands.Bot]):
        self.session = aiohttp.ClientSession(headers = {"Authorization" : "Bot {}".format(token)})
        self.application_id = application_id
        self.token = token
        self.v8 = "https://discord.com/api/v8"

    async def request_command(self, json : dict, guild_id : int = None):
        route = "/applications/{}".format(self.application_id)
        route += "/commands" if not guild_id else "/guilds/{}/commands".format(guild_id)
        route = self.v8 + route
        async with self.session.post(route, json = json) as post_response:
            response = await post_response.json()
            return response

    async def delete_command(self, command_id : int, guild_id : int = None):
        route = "/applications/{}".format(self.application_id)
        route += "/commands/{}".format(command_id) if not guild_id else "/guilds/{}/commands/{}".format(guild_id, command_id)
        route = self.v8 + route
        print(route)
        await self.session.delete(route)

    async def ack_heartbeat(self, interaction_id : int, interaction_token : str):
        route = "https://discord.com/api/v8/interactions/{}/{}/callback".format(interaction_id, interaction_token)
        json = {
            "type": 5
        }
        return await self.session.post(route, json = json)




    async def create_command(self, command_name : str, description : str, options : list = None, guild_id : int = None):
        payload = {"name" : command_name, "description" : description, "options" : options or []}
        response = await self.request_command(payload, guild_id)
        return SlashContext(response)

    

    async def close(self):
        return await self.session.close()



        

