# bot.py

""" git commit the changes first. 'git push heroku master' to update server build. 'heroku logs -a pekobotnewob' to see logs """

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
from youtube_dl import YoutubeDL
import urllib.request
import urllib.parse
import re
import datetime
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery
import json
load_dotenv()

""" Gets the discord bot token and server name from .env file """
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

""" Intets are required for bot to see memebrs in the server as of latest discord.py """
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

yt_list = asyncio.Queue()
playlist = []

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
        emoji = ['↗️','↘️','↙️', '↖️']
        for emote in emoji:
            await message.add_reaction(emote)
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


    if message.content == '!peko':
        c_channel = discord.utils.get(message.guild.text_channels, name='novalty')
        """ Returns a list of limit 2 messages """
        messages = await c_channel.history(limit=2).flatten()
        print(pekofy(messages[1].content))
        await message.channel.send(pekofy(messages[1].content))

    if message.content[0:5] == '!play':
        url = ''
        input = message.content[6:]
        total_duration = 0
        songs_to_add = []
        player_list = []
        if '?list=' in input:
            url = input
        elif 'www.youtube.com' in url:
            url = input
        else:
            url = search_parsing(input)
        print(url)
        if '?list=' in url:
            for link in parse_playlist(url,20):
                video = ytvideo(link)
                total_duration += video.seconds
                songs_to_add.append(video)
        else:
            await message.channel.send("Song found: " + url)
            video = ytvideo(url)
            total_duration += video.seconds
            songs_to_add.append(video)
        if total_duration > 600:
            reply = await message.reply('Are you sure peko? The duration is : [' + duration_parsing(total_duration) +']')
            await reply.add_reaction('👍')
            await reply.add_reaction('👎')
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍' and reaction.message == reply
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('Song not added peko!')
                return
        try:
            voice_channel = message.author.voice.channel
            await voice_channel.connect()
        except:
            pass
        for item in songs_to_add:
            await yt_list.put(item)
            playlist.append(item.title)
        if len(songs_to_add) == 1:
            await message.channel.send(f'Song added to list peko~!:\n' + songs_to_add[0].title + ' [Duration: ' + duration_parsing(songs_to_add[0].seconds) + ']')

    if message.content[0:6] == '!clear':
        while playlist:
            await yt_list.get()
            playlist.pop(0)
        for x in client.voice_clients:
                x.stop()
        await message.channel.send('Playlist cleared!')

    if message.content[0:6] == '!queue':
        videos = '\n'.join(video for video in playlist)
        await message.channel.send(f'Playlist peko~!:\n{videos}')

    if message.content[0:5] == '!skip':
        for x in client.voice_clients:
                return x.stop()

    if 'glasses' in message.content.lower():
        reply = await message.reply(glasses)





async def yt_player():
    while True:
        voice_channel = None
        video = await yt_list.get()
        current_track = video.getPlayer()
        for vc in client.voice_clients:
            voice_channel = vc
        while voice_channel.is_playing():
            await sleep(1)
        voice_channel.play(current_track)
        while voice_channel.is_playing():
            await sleep(1)
        playlist.pop(0)

@loop(seconds=60)
async def yt_stopper():
    if client.voice_clients:
        if client.voice_clients[0].is_playing():
                pass
        else:
            await client.voice_clients[0].disconnect()
yt_stopper.start()

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
        self.duration = duration_parsing(data.get('duration'))
        self.seconds = data.get('duration')

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


def duration_parsing(input):
    return str(datetime.timedelta(seconds=input))


glasses = "I gotchu Takes a deep breath.\nGlasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist's glasses and putting them on like, \"Haha, got your glasses!\" That's just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?"


def parse_playlist(url, max_size):
    url_list = []
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyDZOcdGIepf75qkTS0stb6f_-5XsUB5INs")
    request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = 50)
    response = request.execute()
    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)
        for t in playlist_items:
            link = f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'
            print(link)
            if link not in url_list:
                if len(url_list)>max_size:
                    break
                url_list.append(link)
    return url_list

class ytplaylist:
    def __init__(self,url):
        self.url = url
        self.duration = 0
        self.videoList = self.parse_playlist(url,50)
        self.ytvideolist = self.ytvideoList(self.videoList)


    @classmethod
    def parse_playlist(url, max_size):
        url_list = []
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyDZOcdGIepf75qkTS0stb6f_-5XsUB5INs")
        request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,maxResults = max_size)
        response = request.execute()
        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)
            for t in playlist_items:
                link = f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}'
                print(link)
                if link not in url_list:
                    url_list.append(link)
        return url_list

    @classmethod
    def ytvideoList(self,input):
        output = []
        for link in input:
                video = ytvideo(link)
                output.append(video)
                self.duration += video.seconds
        return output

class ytvideo:
    def __init__(self,url):
        self.url = url
        self.data = self.getdata()
        self.duration = self.data['contentDetails']['duration']
        self.title = self.data['snippet']['title']
        self.seconds = self.ytDurationToSeconds()
    @classmethod
    async def getPlayer(self):
        return await YTDLSource.from_url(self.url, loop=client.loop)

    @classmethod
    def getdata(self):
        video_id = self.url.replace('https://www.youtube.com/watch?v=','')
        api_key="AIzaSyDZOcdGIepf75qkTS0stb6f_-5XsUB5INs"
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails&part=snippet"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data=data['items'][0]
        return all_data
    
    @classmethod
    def ytDurationToSeconds(self):
        week = 0
        day  = 0
        hour = 0
        min  = 0
        sec  = 0
        duration = self.duration.lower()
        value = ''
        for c in duration:
            if c.isdigit():
                value += c
                continue
            elif c == 'p':
                pass
            elif c == 't':
                pass
            elif c == 'w':
                week = int(value) * 604800
            elif c == 'd':
                day = int(value)  * 86400
            elif c == 'h':
                hour = int(value) * 3600
            elif c == 'm':
                min = int(value)  * 60
            elif c == 's':
                sec = int(value)

            value = ''
        return week + day + hour + min + sec


def getdata(url):
    video_id = url.replace('https://www.youtube.com/watch?v=','')
    api_key="AIzaSyDZOcdGIepf75qkTS0stb6f_-5XsUB5INs"
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails&part=snippet"
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items'][0]
    return all_data

def ytDurationToSeconds(duration): #eg P1W2DT6H21M32S
    week = 0
    day  = 0
    hour = 0
    min  = 0
    sec  = 0
    duration = duration.lower()
    value = ''
    for c in duration:
        if c.isdigit():
            value += c
            continue
        elif c == 'p':
            pass
        elif c == 't':
            pass
        elif c == 'w':
            week = int(value) * 604800
        elif c == 'd':
            day = int(value)  * 86400
        elif c == 'h':
            hour = int(value) * 3600
        elif c == 'm':
            min = int(value)  * 60
        elif c == 's':
            sec = int(value)

        value = ''
    return week + day + hour + min + sec



client.loop.create_task(yt_player())
client.run(TOKEN)