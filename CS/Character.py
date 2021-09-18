
import discord




class CS_Character():
    def __init__(self, rowtype, gsheet):
        self.cls = rowtype[1]
        self.data = gsheet.worksheet(self.cls).row_values(rowtype[0] + 1)
        self.name = self.data[1]
        self.rarity = self.data[2]
        self.cost = self.data[3]
        self.type = self.data[4]
        self.atktype = self.data[5]
        self.pve = self.data[6]
        self.raid = self.data[7]
        self.gcoop = self.data[8]
        self.shall = self.data[9]
        self.cbattle = self.data[10]
        self.rpvp = self.data[11]
        self.spvp = self.data[12]
        self.overall = self.data[13]
        self.set = self.data[15]
        self.skill = self.data[16]
        try:
            self.notes = self.data[19]
        except:
            self.notes = ''
            
    classmethod
    def embedconstructor(self):
        embed = discord.Embed(
            title=self.name, description=self.notes, color=0xFF5733)
        embed.add_field(name="Type", value=self.type, inline=True)
        embed.add_field(name="Class", value=self.cls, inline=True)
        embed.add_field(name="Rarity", value=self.rarity, inline=True)
        embed.add_field(name="Cost", value=self.cost, inline=True)
        embed.add_field(name="Attack Type", value=self.atktype, inline=True)
        embed.add_field(name="Overall", value=self.overall, inline=True)

        embed.add_field(name="Story", value=self.pve, inline=True)
        embed.add_field(name="Raid", value=self.raid, inline=True)
        embed.add_field(name="\u200B", value='\u200B', inline=True)

        embed.add_field(name="Guild Co-op", value=self.gcoop, inline=True)
        embed.add_field(name="Shadow Hall", value=self.shall, inline=True)
        embed.add_field(name="Clash Battle", value=self.cbattle, inline=True)

        embed.add_field(name="Ranked PVP", value=self.rpvp, inline=True)
        embed.add_field(name="Strategy PVP", value=self.spvp, inline=True)
        embed.add_field(name="\u200B", value='\u200B', inline=True)

        embed.add_field(name="Gear Recc.", value=self.set, inline=True)
        embed.add_field(name="Skills", value=self.skill, inline=True)
        embed.add_field(name="\u200B", value='\u200B', inline=True)

        embed.set_footer(
            text="https://docs.google.com/spreadsheets/d/1eN8YLqAvzYTHP3V9yv1BYV0kMKJa-FdhW-_qaj2QDJA/")

        return embed


    ###For offline testing
    classmethod
    def test(self):
        print(self.name)
        print(self.cls)
        print(self.rarity)
        print(self.overall)

