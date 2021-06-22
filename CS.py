import gspread
import discord

gc = gspread.service_account(filename='creds.json')
gsheet = gc.open_by_key("1eN8YLqAvzYTHP3V9yv1BYV0kMKJa-FdhW-_qaj2QDJA")

classes = ["Defender", "Striker", "Ranger", "Sniper", "Support", "Siege", "Tower"]

def chara_search(name):
    data = []
    characters = []
    for type in classes:
        temp = gsheet.worksheet(type)
        data.append(temp)
    for type in data:
        mylist = type.col_values(2)
        for i in range(len(mylist)):
            if (mylist[i].lower().count(name.lower())>0):
                values_list = type.row_values(i + 1)
                characters.append(parsing(type.title, values_list))
    return characters


def parsing(unit, data):
    character = {
        "class": unit
    }
    character['name'] = data[1]
    character['rarity'] = data[2]
    character['cost'] = data[3]
    character['type'] = data[4]
    character['atktype'] = data[5]
    character['pve'] = data[6]
    character['raid'] = data[7]
    character['gcoop'] = data[8]
    character['shall'] = data[9]
    character['cbattle'] = data[10]
    character['rpvp'] = data[11]
    character['spvp'] = data[12]
    character['overall'] = data[13]
    character['set'] = data[15]
    character['skill'] = data[16]
    try:
        character['notes'] = data[19]
    except:
        character['notes'] = ''

    return character

def chara_formatting(data):
    embed=discord.Embed(title=data['name'], description=data['notes'], color=0xFF5733)
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

    embed.set_footer(text="https://docs.google.com/spreadsheets/d/1eN8YLqAvzYTHP3V9yv1BYV0kMKJa-FdhW-_qaj2QDJA/")

    return embed




