import discord
from discord.ext.tasks import loop
import asyncio
from asyncio import sleep
from spotify import spotify_parsing
from yt import ytplaylist
from yt import ytvideo
from datetime import timedelta
from yt_new import pytubemp3



class mediaQueue():
    def __init__(self):
        self.yt_list = asyncio.Queue()
        self.playlist = []


    classmethod
    async def playCommand(self, client, message):
        input = message.content[6:]
        total_duration = 0
        songs_to_add = []
        print(input)
        if 'spotify' in input:
            song_list = spotify_parsing(input)
            for item in song_list:
                video = ytvideo(item)
                total_duration += video.seconds
                songs_to_add.append(video)
        elif '&list=' in input or '?list=' in input: #checks if input is a playlist
            videolist = ytplaylist(input) #creates ytplaylist object from input url
            songs_to_add.extend(videolist.ytvideolist) #appends the list of ytvideo objects in videolist ot songs_to_add
            total_duration += videolist.seconds
        else:
            video = ytvideo(input) #creates yt video object
            await message.channel.send(f"Song found: {video.url}")
            total_duration += video.seconds
            songs_to_add.append(video) #appends to pending list of songs from the invocaiton of !play command
        print(total_duration)
        if total_duration > 600:
            reply = await message.reply('Are you sure peko? The duration is : [' + self.duration_parsing(total_duration) +']')
            await reply.add_reaction('👍')
            await reply.add_reaction('👎')
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍' and reaction.message == reply
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('```Song not added peko!```')
                return
        try:
            voice_channel = message.author.voice.channel
            await voice_channel.connect()
        except:
            pass
        await message.delete() #deletes the command message after responding
        for item in songs_to_add:
            await self.yt_list.put(item) #yt_list is an asyncio queue that cna be popped by the play loop
            self.playlist.append(item.title) #playlist is a normal list for normal access
        if len(songs_to_add) == 1:
            await message.channel.send(f'```Song added to list peko~!:\n' + songs_to_add[0].title + ' [Duration: ' + self.duration_parsing(songs_to_add[0].seconds) + ']' + '[Requested by: ' + message.author.name + ']```')
    classmethod
    async def clearCommand(self, client, message):
        while len(self.playlist) > 1: #remove everything from the asyncio playlist and normal playlist
            self.playlist.pop(0)
            await self.yt_list.get()
        self.playlist.pop(0) #do the final pop from normal list to avoid erros with asyncio queue
        for x in client.voice_clients: #this removes the final item from asyncio queue
                x.stop()
        await message.channel.send('```Playlist cleared!```')

    async def queueCommand(self,message):
        await self.print_playlist(self.playlist, message.channel)

    async def skipCommand(self,client, message):
        if message.content == '!skip':  # stops the current song. playlist is handled by playback loop
            for x in client.voice_clients:
                return x.stop()
        elif message.content[0:5] == '!skip':  # uses lazy deletion in the regular list. actual skip is handled by the playback loop
            entry = int(message.content[6:])
            self.playlist.pop(entry)
            await self.print_playlist(self.playlist, message.channel)

    """Method to convert a time into a String"""
    classmethod
    def duration_parsing(self, input):
        return str(timedelta(seconds=input))

    """Method to handle display of the music playlist"""
    classmethod
    async def print_playlist(self,list, channel):  # builds playlist string
        videos = ""
        for i in range(len(list)):
            if i == 0:
                videos += '\nCurrent Song:\n' + self.playlist[i]
                videos += '\n\nPlaylist:'
            else:
                videos += '\n' + str(i) + '. ' + self.playlist[i]
        await channel.send(f'```{videos}```')

    classmethod
    async def getTrack(self):
        return await self.yt_list.get()
    classmethod
    def firstTrack(self):
        return self.playlist[0]
    classmethod
    def popTrack(self):
        self.playlist.pop(0)






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
async def yt_player(parser, client): #yt player loop/task
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
            await c_channel.send(f"```Now playing: {video.title}```")
        else:
            continue #do nothing and end the run of the loop if the first video is not the same as the popped queue item
        while voice_channel.is_playing():
            await sleep(1)
        try:
            temp.deleteMP3()
            parser.mediaQueue.popTrack()
        except:
            pass


