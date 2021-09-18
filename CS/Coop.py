
import discord



class coop():
    def __init__(self):
        self.first = "1"
        self.second = "2"
        self.tips = ""
    classmethod
    def setFirst(self, message):
        self.first = message[7:]
    classmethod
    def setSecond(self, message):
        self.first = message[7:]
    classmethod
    def setSecond(self, message):
        self.first = message[7:]

    classmethod
    def coopMessage(self, message):
        embed = discord.Embed(title="Consortium Co-op Battle", url="",
                                  description="Please hit tha arenas listed and wait till Sunday to hit the boss!",
                                  color=0xFF5733)
        embed.set_thumbnail(url="https://imgur.com/EM9OQJv")
        embed.add_field(name="First Priority", value=self.first, inline=True)
        embed.add_field(name="Second Priority", value=self.second, inline=True)
        embed.set_footer(text=self.tips)