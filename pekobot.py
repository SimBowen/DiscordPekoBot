# bot.py

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from asyncio import sleep

load_dotenv()

""" Gets the discord bot token and server name from .env file """
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

""" Intets are required for bot to see memebrs in the server as of latest discord.py """
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!')


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

    print("Members in the guild are: \n")
    for name in guild.members:
        print(name)


    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

""" Triggers upon memeber join event """
""" @client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'こんにちは {member.name}, いらっしゃいぺこ!'
    ) """

""" Triggers upon message and checks current message """

""" @client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!peko':
        test = pekofy(message.author.lastMessage.content)
        response = pekofy(previous_message)
        print(response)
        await message.channel.send(response) """

""" Triggers on message, checks if there were previous messages to parse."""
@client.event
async def on_message(message):
    if 'haha' in message.content:
        response = "AH↗️HA↘️HA↗️HA↘️HA↗️HA↘️HA↗️HA↘️"
        await message.channel.send(response)
        """ Gets author's vc if they are in one  """
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            voice_channel = None
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(f'haha.mp3'))
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
        else:
            print(str(message.author.name) + " is not in a channel.")
    
    if 'yep' in message.content:
        await message.add_reaction(':YEPCOCK:')
    c_channel = discord.utils.get(message.guild.text_channels, name='novalty')
    """ Returns a list of limit 2 messages """
    messages = await c_channel.history(limit=2).flatten()
    if message.content == '!peko':
        print(pekofy(messages[1].content))
        await message.channel.send(pekofy(messages[1].content))




""" pekofy splitter """
def pekofy(input):
    output = input
    delimiters = ['.',',','!','?']
    res = any(ele in delimiters for ele in input)
    if res:
        output = output.replace("."," peko.")
        output = output.replace(","," peko,")
        output = output.replace("!"," peko!")
        output = output.replace("?"," peko?")
    else:
        output += " peko."
    return output


client.run(TOKEN)