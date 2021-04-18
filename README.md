# slash-ext

Yet another slash command lib made for discord.py, except this one intergrates will intergrate with `discord.ext`, thus making it a lot easier to use. Some resources are provided too, such as the `INTERACTION_CREATE` socket response. This is provided in the `debug.json` file. I do not mind sharing this token as its invalid.


Example:
```py
import discord
from discord.ext import commands, slash
from discord.ext.slash.abc import SlashContext

bot = commands.Bot(command_prefix="!", case_insensitive=True)
slashParent = slash.SlashBot(bot, "<bot token>", 770301542170361896) #<= Bot User ID

@bot.event
async def on_ready():
    print("Ready!")


@slashParent.slash_command(name="rachel", description="hola", guild_ids=[830418497837203457]) #make sure to not have names with spaces in them as discord will not create them.
async def dummy(ctx: SlashContext):
    embeds = [discord.Embed(title = "Hello World")]
    await ctx.send(content= "Hello World", embeds=embeds)
    await ctx.edit(content= "Hello Discord")


@bot.event
async def on_slash_recieve(payload): #=> event that is fired when a slash command is fired and it is found in the bot's cache
    print("RECEIEVED SLASH")
    print(payload)

bot.run("<bot token>")
```

We give you the option to pass in the bot token and bot user id because you cannot access the `token` and `id` before the bot is ready.
If you have any questions, please DM me on Discord: moonie#6598
