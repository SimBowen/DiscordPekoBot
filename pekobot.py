# bot.py

""" git commit the changes first. 'git push heroku master' to update server build. 'heroku logs -a pekobotnewob' to see logs """
import os
import discord
from discord.ext.tasks import loop
from dotenv import load_dotenv
from MediaCommands import yt_player
from MessageParser import MessageParser

load_dotenv()

""" Gets the discord bot token and server name from .env file """
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

""" Intets are required for bot to see memebrs in the server as of latest discord.py """
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

parser = MessageParser()


""" Upon client startup event run the following code """
@client.event
async def on_ready():
    """ Loop thorugh to find server names if required """
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

""" Triggers on message, checks if there were previous messages to parse."""
@client.event
async def on_message(message):
    await parser.parseMessage(client, message)


@loop(seconds=154) #Checks if anything is playing every few minutes. If nothing, disconnect bot.
async def yt_stopper():
    if client.voice_clients:
        if client.voice_clients[0].is_playing():
                pass
        else:
            await client.voice_clients[0].disconnect()

yt_stopper.start()
client.loop.create_task(yt_player(parser, client)) #get the ytplay task to run in a loop
client.run(TOKEN)
