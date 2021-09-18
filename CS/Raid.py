import discord
import pytz
from datetime import datetime

class raid():
    def __init__(self, message):
        self.requestor = message.author
        self.message = message.content.split(' ')
        try:
            self.level = float(self.message[1]) 
        except:
            raise Exception("Invalid raid command format!")
        self.GMT8 = pytz.timezone('Asia/Singapore')
        self.time = datetime.now(self.GMT8)

    classmethod
    def start(self):
        embed = discord.Embed(title="Raid Alert!", url="",
                          description="This is a raid alert. Kindly enter and wait for 3 minutes before killing the raid boss!",
                          color=0xFF5733)
        embed.set_author(name=self.requestor, url="")
        embed.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
        embed.add_field(name="Level", value=self.level, inline=True)
        embed.add_field(name="Time Sent (GMT+8)",
                    value=self.time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.add_field(name="Status", value="Valid")
        embed.set_footer(text="This message will time out 3 minutes after the time it was sent!")
        return embed

    classmethod
    def end(self):
        embedupdate = discord.Embed(title="Old Raid", url="", description="This is an old raid alert.",
                                color=0xFF5733)
        embedupdate.set_author(name=self.requestor, url="")
        embedupdate.set_thumbnail(url="https://i.imgur.com/xpUtROZ.png")
        embedupdate.add_field(name="Level", value=self.level, inline=True)
        embedupdate.add_field(name="Time Sent (GMT+8)",
                          value=self.time.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embedupdate.add_field(name="Status", value="Expired")
        return embedupdate
