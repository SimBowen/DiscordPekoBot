# bot.py
from asyncio.windows_events import NULL
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!peko')

previous_message = 'test'


@client.event
async def on_ready():
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

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'こんにちは {member.name}, いらっしゃいぺこ!'
    )


""" @client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!peko':
        test = pekofy(message.author.lastMessage.content)
        response = pekofy(previous_message)
        print(response)
        await message.channel.send(response) """

@client.event
async def on_message(message):
    c_channel = discord.utils.get(message.guild.text_channels, name='general')
    messages = await c_channel.history(limit=2).flatten()
    if(messages[1] != NULL):
        print(messages[1].content)
    if messages[0].content == '!peko':
        if(messages[1] == NULL):
            print('nothing')
            return
        else:
            print(pekofy(messages[1].content))
            await message.channel.send(pekofy(messages[1].content))




    


def pekofy(input):
    output = ""
    x = input.split(".")
    if(len(x)==0):
        output = input + " peko."
    else:
        for word in x:
            if word == '':
                continue
            output += word + " peko."
    return output


client.run(TOKEN)