import discord
import pytz
from datetime import datetime, timedelta


def cs_chara(data):
    embed = discord.Embed(title=data['name'],
                          description=data['notes'], color=0xFF5733)
    embed.add_field(name="Type", value=data['type'], inline=True)
    embed.add_field(name="Class", value=data['class'], inline=True)
    embed.add_field(name="Rarity", value=data['rarity'], inline=True)
    embed.add_field(name="Cost", value=data['cost'], inline=True)
    embed.add_field(name="Attack Type", value=data['atktype'], inline=True)
    embed.add_field(name="Overall", value=data['overall'], inline=True)

    embed.add_field(name="Story", value=data['pve'], inline=True)
    embed.add_field(name="Raid", value=data['raid'], inline=True)
    embed.add_field(name="\u200B", value='\u200B', inline=True)

    embed.add_field(name="Guild Co-op", value=data['gcoop'], inline=True)
    embed.add_field(name="Shadow Hall", value=data['shall'], inline=True)
    embed.add_field(name="Clash Battle", value=data['cbattle'], inline=True)

    embed.add_field(name="Ranked PVP", value=data['rpvp'], inline=True)
    embed.add_field(name="Strategy PVP", value=data['spvp'], inline=True)
    embed.add_field(name="\u200B", value='\u200B', inline=True)

    embed.add_field(name="Gear Recc.", value=data['set'], inline=True)
    embed.add_field(name="Skills", value=data['skill'], inline=True)

    embed.set_footer(
        text="https://docs.google.com/spreadsheets/d/1eN8YLqAvzYTHP3V9yv1BYV0kMKJa-FdhW-_qaj2QDJA/")

    return embed


async def raid(author, message):
    embeds = []
    by = author
    input = message.lower()
    elements = input.split(' ')
    try:
        level = elements[1]
        float(level)
    except:
        raise Exception("Invalid raid command format!")
    GMT8 = pytz.timezone('Asia/Singapore')
    time = datetime.now(GMT8)
    embed = discord.Embed(title="Raid Alert!", url="",
                          description="This is a raid alert. Kindly enter and wait for 3 minutes before killing the raid boss!",
                          color=0xFF5733)
    embed.set_author(name=by.display_name, url="")
    embed.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Time Sent (GMT+8)",
                    value=time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    embed.add_field(name="Status", value="Valid")
    embed.set_footer(
        text="This message will time out 3 minutes after the time it was sent!")

    embeds.append(embed)

    embedupdate = discord.Embed(title="Old Raid", url="", description="This is an old raid alert.",
                                color=0xFF5733)
    embedupdate.set_author(name=by.display_name, url="")
    embedupdate.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
    embedupdate.add_field(name="Level", value=level, inline=True)
    embedupdate.add_field(name="Time Sent (GMT+8)",
                          value=time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
    embedupdate.add_field(name="Status", value="Expired")

    embeds.append(embedupdate)



def musicEmbed(ytvideo, index):
    embed = discord.Embed(title=ytvideo.title,description=ytvideo.url, color=0xFF5733)
    embed.set_author(name=ytvideo.requestor, url="")
    embed.set_thumbnail(url=ytvideo.thumbnail)
    embed.add_field(name="Duration", value=ytvideo.time, inline=True)
    embed.add_field(name="Pos. in Queue", value=index, inline=True)
    return embed

def nowPlaying(ytvideo):
    embed = discord.Embed(title=ytvideo.title,description=ytvideo.url, color=0xFF5733)
    embed.set_author(name="Now Playing:", url="")
    embed.set_thumbnail(url=ytvideo.thumbnail)
    embed.add_field(name="Duration", value=ytvideo.time, inline=True)
    embed.add_field(name="Requested by", value=ytvideo.requestor, inline=True)
    return embed


def queueEmbed(queue):
    try:
        current_track = queue[0]
        current_title = current_track.title
        current_url = current_track.url
        current_requestor = current_track.requestor
        current_thumbnail = current_track.thumbnail
    except:
        current_title = '-'
        current_url = '-'
        current_requestor = '-'
        current_thumbnail = '-'
    embed = discord.Embed(title=current_title,description=current_url, color=0xFF5733)
    embed.set_author(name=current_requestor, url="")
    embed.set_thumbnail(url=current_thumbnail)

    songs = ''
    duration = ''
    requestor = ''
    if(len(queue) < 2):
        songs = '-'
        duration = '-'
        requestor = '-'
    else:
        for i in range(len(queue)):
            wrap = len(queue[i].title) // 25
            songs += str(i) + '. ' + queue[i].title + '\n'
            duration += queue[i].time + '\n'             
            requestor += str(queue[i].requestor) + '\n'
            for i in range(wrap):
                duration+= '\n'
                requestor+='\n'
    embed.add_field(name="Title", value=songs, inline=True)
    embed.add_field(name="Duration", value=duration, inline=True)
    embed.add_field(name="Requestor", value=requestor)
    return embed


    

