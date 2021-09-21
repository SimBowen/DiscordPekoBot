from MessageHandlers.embeds import cshelpEmbed, musichelpEmbed
import random
import discord
from Media.MediaHandlers import play_mp3
from discord.ext.tasks import loop

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

async def haha(message):
    emoji = ['↗️','↘️','↙️', '↖️'] #holds the reaction emojis
    for emote in emoji:
        await message.add_reaction(emote)
    n = random.randint(1,11)
    """takes a random mp3 file"""
    file = "haha" + str(n) + ".mp3"
    await play_mp3(file,message) #awaits the invocation of play_mp3 method
async def horny(message):
    await play_mp3("horny.mp3", message) #awaits the invocation of play_mp3 method
async def ehe(message):
    await play_mp3("ehe.mp3", message) #awaits the invocation of play_mp3 method
async def pekora(message):
    await play_mp3("pekora.mp3", message)
async def friend(message):
    await play_mp3("friend.mp3", message)
async def yep(message):
    await reactCustom(message,792035440428974111)
async def hmm(message):
    await react(message,'🤔')
async def glasses(message):
    await respond(message,"I gotchu Takes a deep breath.\nGlasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist's glasses and putting them on like, \"Haha, got your glasses!\" That's just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?",[])
async def dragon(message):
    await respond(message,"Dragon deez nuts on your face peko~!",['↗️','↘️','↙️', '↖️'])
async def peko(message):
    c_channel = discord.utils.get(message.guild.text_channels, name='novalty') #Set specific text channel ot monitor for messages
    messages = await c_channel.history(limit=2).flatten() #Grab the 2nd last message in channel
    await message.channel.send(pekofy(messages[1].content)) #invokes pekofy and sends



"""Method to Pekofy a String"""
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

async def respond(message,replytext,emoji=[]):
    if (message.author != client.user):
        reply = await message.reply(replytext)
        for emote in emoji:
            await reply.add_reaction(emote)

async def reactCustom(message,emojiID):
    emoji = client.get_emoji(emojiID)  # grab the emoji
    await message.add_reaction(emoji)

"""Method to react to a message with a string and react to the response with standard emojis"""
async def react(message,emoji):
    await message.add_reaction(emoji)


async def helpCommand(message):
   await message.channel.send(embed = musichelpEmbed())
   await message.channel.send(embed = cshelpEmbed()) 

async def cshelpCommand(message):
   await message.channel.send(embed = cshelpEmbed()) 