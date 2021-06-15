# bot.py

""" git commit the changes first. 'git push heroku master' to update server build. 'heroku logs -a pekobotnewob' to see logs """
import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from asyncio import sleep
import random
import datetime
from urllib.parse import parse_qs, urlparse
from yt import ytvideo
from yt import ytplaylist
from yt import YTDLSource
from spotify import spotify_parsing
import random
import pytz
from datetime import datetime
from CS import chara_search
from CS import chara_formatting
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
        emoji = ['↗️','↘️','↙️', '↖️'] #holds the reaction emojis
        for emote in emoji:
            await message.add_reaction(emote)
        n = random.randint(1,10)
        """takes a random mp3 file"""
        file = "haha" + str(n) + ".mp3"
        await play_mp3(file,message) #awaits the invocation of play_mp3 method
    if 'horny' in message.content.lower():
        await play_mp3("horny.mp3", message) #awaits the invocation of play_mp3 method

    if 'ehe' in message.content.lower():
        await play_mp3("ehe.mp3", message) #awaits the invocation of play_mp3 method

    if 'pekora' in message.content.lower():
        await play_mp3("pekora.mp3", message)

    if 'friend' in message.content.lower():
        await play_mp3("friend.mp3", message)

    if 'yep' in message.content.lower():
        id = 792035440428974111 #set emoji id
        emoji = client.get_emoji(id) #grab the emoji
        await message.add_reaction(emoji)

    if message.content == '!peko':
        c_channel = discord.utils.get(message.guild.text_channels, name='novalty') #Set specific text channel ot monitor for messages
        messages = await c_channel.history(limit=2).flatten() #Grab the 2nd last message in channel
        await message.channel.send(pekofy(messages[1].content)) #invokes pekofy and sends

    if message.content[0:5] == '!play':
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
            reply = await message.reply('Are you sure peko? The duration is : [' + duration_parsing(total_duration) +']')
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
            await yt_list.put(item) #yt_list is an asyncio queue that cna be popped by the play loop
            playlist.append(item.title) #playlist is a normal list for normal access
        if len(songs_to_add) == 1:
            await message.channel.send(f'```Song added to list peko~!:\n' + songs_to_add[0].title + ' [Duration: ' + duration_parsing(songs_to_add[0].seconds) + ']' + '[Requested by: ' + message.author.name + ']```')

    if message.content[0:6] == '!clear':
        while len(playlist) > 1: #remove everything from the asyncio playlist and normal playlist
            playlist.pop(0)
            await yt_list.get()
        playlist.pop(0) #do the final pop from normal list to avoid erros with asyncio queue
        for x in client.voice_clients: #this removes the final item from asyncio queue
                x.stop()
        await message.channel.send('```Playlist cleared!```')

    if message.content[0:6] == '!queue': #invokes print playlist method. Needs to be awaited as it prints a message
        await print_playlist(playlist, message.channel)

    if message.content == '!skip': #stops the current song. playlist is handled by playback loop
        for x in client.voice_clients:
                return x.stop()
    elif message.content[0:5] == '!skip': #uses lazy deletion in the regular list. actual skip is handled by the playback loop
        entry = int(message.content[6:])
        playlist.pop(entry)
        await print_playlist(playlist, message.channel)
    
    if "!raid" in message.content.lower() and message.author != client.user:
        by = message.author
        input = message.content.lower()
        elements = input.split(' ')
        try:
            level = elements[1]
            float(level)
        except:
            await message.reply("Invalid raid command format!")
            return
        GMT8 = pytz.timezone('Asia/Singapore')
        time = datetime.now(GMT8)
        embed=discord.Embed(title="Raid Alert!", url="", description="This is a raid alert. Kindly enter and wait for 3 minutes before killing the raid boss!", color=0xFF5733)
        embed.set_author(name=by.display_name, url="")
        embed.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="Time Sent (GMT+8)", value=time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.add_field(name="Status", value="Valid")
        embed.set_footer(text="This message will time out 3 minutes after the time it was sent!")
        alert = await message.channel.send(embed=embed)
        await message.delete()
        await alert.add_reaction('👍')
        embedupdate=discord.Embed(title="Old Raid", url="", description="This is an old raid alert.", color=0xFF5733)
        embedupdate.set_author(name=by.display_name, url="")
        embedupdate.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
        embedupdate.add_field(name="Level", value=level, inline=True)
        embedupdate.add_field(name="Time Sent (GMT+8)", value=time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embedupdate.add_field(name="Status", value="Expired")
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍' and reaction.message == alert
        try:
            await client.wait_for('reaction_add', timeout=180.0, check=check)
            embedupdate.set_footer(text="Raid boss has been killed!")
            await alert.edit(embed = embedupdate)
            return 
        except asyncio.TimeoutError:
            embedupdate.set_footer(text="3 minutes has elapsed. Raid boss may have been killed!")
            await alert.edit(embed = embedupdate)
            return

    if "!cs" in message.content.lower():
        search = message.content[4:]
        characters = chara_search(search)
        if characters == []:
            await message.channel.send("Invalid search!")
            return
        for character in characters:
            embed = chara_formatting(character)
            await message.channel.send(embed=embed)
        


    if 'glasses' in message.content.lower(): #Glasses.
        reply = await message.reply(glasses)

    if 'dragon' in message.content.lower():

        if message.author != client.user:
            reply = await message.reply("Dragon deez nuts on your face peko~!")
            emoji = ['↗️','↘️','↙️', '↖️']
            for emote in emoji:
                await reply.add_reaction(emote)



async def print_playlist(list, channel): #builds playlist string
    videos = ""
    for i in range(len(list)):
        if i == 0:
            videos += '\nCurrent Song:\n' + playlist[i]
            videos += '\n\nPlaylist:'
        else:
            videos += '\n' + str(i) + '. ' + playlist[i]
    await channel.send(f'```{videos}```')

async def yt_player(): #yt player loop/task
    while True:
        voice_channel = None
        video = await yt_list.get() #pops the first ytvideo object from asyncio queue
        current_track = await YTDLSource.from_url(video.url, loop=client.loop) #"player" is created using the method contained in YTDLSource. URL is extracted from ytvideo object
        for vc in client.voice_clients: #Only works if bot is currently in voice channel. To be improved
            voice_channel = vc
        while voice_channel.is_playing():#Puts bot to sleep while track is playing. Stops bot from trying to play multiple songs at once due to loop
            await sleep(1)
        if(current_track.title == playlist[0]): #Lazy deletion is checked here. Checks if popped ytvideo name matches the first object in playlist. If so, play. 
            voice_channel.play(current_track)
            c_channel = discord.utils.get(client.guilds[0].text_channels, name='radio') #retreives a specific text channel
            await c_channel.send(f"```Now playing: {video.title}```")
        else:
            continue #do nothing and end the run of the loop if the first video is not the same as the popped queue item
        while voice_channel.is_playing():
            await sleep(1)
        try:
            playlist.pop(0)
        except:
            pass


@loop(seconds=154) #Checks if anythin gis playing every few minutes. If nothing, disconnect bot.
async def yt_stopper():
    if client.voice_clients:
        if client.voice_clients[0].is_playing():
                pass
        else:
            await client.voice_clients[0].disconnect()
yt_stopper.start()

""" pekofy splitter """
def pekofy(input): #Peko.
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




def duration_parsing(input):
    return str(datetime.timedelta(seconds=input))


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


glasses = "I gotchu Takes a deep breath.\nGlasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist's glasses and putting them on like, \"Haha, got your glasses!\" That's just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?"

client.loop.create_task(yt_player()) #get the ytplay task to run in a loop
client.run(TOKEN)