
from CS.Database import CS_Database
from MediaCommands import mediaQueue
from MessageReactions import *

class MessageParser:
    def __init__(self):
        self.commandList = ["haha","horny","ehe","pekora","friend",
                        "yep","hmm","glasses","dragon","!cs","!play","!skip","!queue","!clear"]
        self.cs = CS_Database()
        self.mediaQueue = mediaQueue()

    classmethod
    def parseCommand(self, message):
        for command in self.commandList:
            if command in message.content.lower():
                return str(command)
    classmethod
    async def parseMessage(self, client, message):
        command = str(self.parseCommand(message))
        if '!' in command:
            await self.commandParser(client, command, message)
        else:
            await self.reactionParser(command, message)

    classmethod            
    async def commandParser(self, client, command, message):
        if command == "!cs":
            await self.cs.searchCommand(message)
        elif command == "!play":
            await self.mediaQueue.playCommand(client, message) 
        elif command == "!skip":
            await self.mediaQueue.skipCommand(client, message)
        elif command == "!clear":
            await self.mediaQueue.clearCommand(client, message)
        elif command == "!queue":
            await self.mediaQueue.queueCommand(message)    
    

    async def reactionParser(self, command,  message):
        try:
            await globals()[command](message)
        except:
            pass 
