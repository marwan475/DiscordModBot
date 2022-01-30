import discord
from discord.ext import commands
from discord.utils import get
import music

TOKEN = ""

cogs = [music]

client = commands.Bot(command_prefix="!",intents=discord.Intents.all())
for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))





client.run(TOKEN)