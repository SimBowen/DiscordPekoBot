import discord
import pytz
from datetime import datetime


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