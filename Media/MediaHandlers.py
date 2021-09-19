from MessageHandlers.embeds import nowPlaying
import discord
from asyncio import sleep
from Media.pytube import pytubemp3
from Media.ytdl import YTDLSource




async def play_mp3(mp3, message): #takes in the mp3 file name and message data.
    try:
        voice_channel = message.author.voice.channel # obtain the vc of author if applicable
    except AttributeError:
        voice_channel = None
    channel = None
    if voice_channel != None: 
        channel = voice_channel.name
        vc = await voice_channel.connect() #connect to vc of message author
        vc.play(discord.FFmpegPCMAudio(mp3)) #play mp3
        while vc.is_playing():
            await sleep(1)
        await vc.disconnect()
    else:
        print(str(message.author.name) + " is not in a channel.")



"""Method to handle youtube player"""
async def pytube_player(parser, client): #yt player loop/task
    while True:
        voice_channel = None
        video = await parser.mediaQueue.getTrack() #pops the first ytvideo object from asyncio queue
        current_track = video.title  #"player" is created using the method contained in YTDLSource. URL is extracted from ytvideo object
        temp = pytubemp3(video.url)
        for vc in client.voice_clients: #Only works if bot is currently in voice channel. To be improved
            voice_channel = vc
        while voice_channel.is_playing():#Puts bot to sleep while track is playing. Stops bot from trying to play multiple songs at once due to loop
            await sleep(1)
        if(current_track == parser.mediaQueue.firstTrack()): #Lazy deletion is checked here. Checks if popped ytvideo name matches the first object in playlist. If so, play.
            print("extracting")
            temp.extractMP3()
            voice_channel.play(discord.FFmpegPCMAudio('temp.mp3'))
            c_channel = discord.utils.get(client.guilds[0].text_channels, name='radio') #retreives a specific text channel
            embed = nowPlaying(video)
            await c_channel.send(embed = embed)
        else:
            continue #do nothing and end the run of the loop if the first video is not the same as the popped queue item
        while voice_channel.is_playing():
            await sleep(1)
        try:
            temp.deleteMP3()
            parser.mediaQueue.popTrack()
        except:
            pass


async def yt_player(parser, client): #yt player loop/task
    while True:
        voice_channel = None
        video = await parser.mediaQueue.getTrack() #pops the first ytvideo object from asyncio queue
        current_track = await YTDLSource.from_url(video.url, loop=client.loop) #"player" is created using the method contained in YTDLSource. URL is extracted from ytvideo object
        for vc in client.voice_clients: #Only works if bot is currently in voice channel. To be improved
            voice_channel = vc
        while voice_channel.is_playing():#Puts bot to sleep while track is playing. Stops bot from trying to play multiple songs at once due to loop
            await sleep(1)
        if(current_track.title == parser.mediaQueue.firstTrack()): #Lazy deletion is checked here. Checks if popped ytvideo name matches the first object in playlist. If so, play.
            voice_channel.play(current_track)
            c_channel = discord.utils.get(client.guilds[0].text_channels, name='radio') #retreives a specific text channel
            embed = nowPlaying(video)
            await c_channel.send(embed = embed)
        else:
            continue #do nothing and end the run of the loop if the first video is not the same as the popped queue item
        while voice_channel.is_playing():
            await sleep(1)
        try:
            parser.mediaQueue.popTrack()
        except:
            pass
