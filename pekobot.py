# bot.py

#Testing

""" git commit the changes first. 'git push heroku master' to update server build. 'heroku logs -a pekobotnewob' to see logs """
""" Testing """

import asyncio
from discord.errors import ClientException
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.tasks import loop
from asyncio import sleep
import random
import youtube_dl
import urllib.request
import urllib.parse
import re
load_dotenv()

""" Gets the discord bot token and server name from .env file """
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

""" Intets are required for bot to see memebrs in the server as of latest discord.py """
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

yt_list = []

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
    if 'haha' in message.content.lower():
        """ response = "AH↗️HA↘️HA↗️HA↘️HA↗️HA↘️HA↗️HA↘️" """
        emoji = ['↗️','↘️','↙️', '↖️']
        for emote in emoji:
            await message.add_reaction(emote)
        """ await message.channel.send(response) """
        """ Gets author's vc if they are in one  """
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            voice_channel = None
        channel = None
        if voice_channel != None:

            haha = ['haha1.mp3', 'haha2.mp3', 'haha3.mp3', 'haha4.mp3', 'haha5.mp3', 'haha6.mp3', 'haha7.mp3']
            channel = voice_channel.name
            vc = await voice_channel.connect()
            file = random.choice(haha)
            print(file)
            vc.play(discord.FFmpegPCMAudio(file))
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
        else:
            print(str(message.author.name) + " is not in a channel.")
    if 'horny' in message.content.lower():
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            voice_channel = None
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('horny.mp3'))
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
        else:
            print(str(message.author.name) + " is not in a channel.")

    if 'ehe' in message.content.lower():
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            voice_channel = None
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('ehe.mp3'))
            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
        else:
            print(str(message.author.name) + " is not in a channel.")

    if 'yep' in message.content.lower():
        """ Find the correct emoji id """
        id = 792035440428974111
        emoji = client.get_emoji(id)
        await message.add_reaction(emoji)

    c_channel = discord.utils.get(message.guild.text_channels, name='novalty')
    """ Returns a list of limit 2 messages """
    messages = await c_channel.history(limit=2).flatten()
    if message.content == '!peko':
        print(pekofy(messages[1].content))
        await message.channel.send(pekofy(messages[1].content))

    if message.content[0:6] == '!pekop':
        url = ''
        input = message.content[7:]
        if input[0:11] == 'youtube.com':
            url = message.content[7:]
        else:
            url = search_parsing(message.content[7:])

        print(url)
        player = await YTDLSource.from_url(url, loop=client.loop)
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            voice_channel = None
        yt_list.append([voice_channel,message.channel, player])
        await message.channel.send('Song added to list:]\n' + player.title)


    if message.content[0:6] == '!pekoq':
        videos = '\n - '.join([video[2].title for video in yt_list])
        await message.channel.send(f'Playlist:\n - {videos}')

    if message.content[0:6] == '!pekos':
        for x in client.voice_clients:
                return await x.disconnect()
        yt_list.pop(0)







@loop(seconds=1)
async def yt_player():
    await client.wait_until_ready()
    if yt_list:
        current_track = yt_list[0]
        voice_channel = current_track[0]
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            try:
                vc = await voice_channel.connect()
            except ClientException:
                print(yt_list)
                return
            vc.play(current_track[2], after=lambda e: print('Player error: %s' % e) if e else None)
            await current_track[1].send('Now playing: {}'.format(current_track[2].title))
            while vc.is_playing():
                    await sleep(1)
            await vc.disconnect()
            yt_list.pop(0)

yt_player.start()




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





ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def search_parsing(input):
    search_keyword=input.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]



client.run(TOKEN)