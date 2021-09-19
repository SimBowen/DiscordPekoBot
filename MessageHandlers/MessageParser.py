
from CS.Database import CS_Database
from MessageHandlers.MediaCommands import mediaQueue
from MessageHandlers.MessageReactions import *

class MessageParser:
    def __init__(self):
        self.commandList = ["haha","horny","ehe","pekora","friend",
                        "yep","hmm","glasses","dragon","!cs","!p","!s","!q","!c","!play","!skip","!queue","!clear"]
        self.cs = CS_Database()
        self.mediaQueue = mediaQueue()

    classmethod
    def parseCommand(self, message):
        i = message.content.find(' ',0)
        if ( i!= -1):
            command = message.content[:i].lower()
        else:
            command = message.content
            print(command)
        if command in self.commandList:
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
        elif command == "!p" or command == "!play":
            await self.mediaQueue.playCommand(client, message) 
        elif command == "!s" or command == "!skip":
            await self.mediaQueue.skipCommand(client, message)
        elif command == "!c" or command == "!clear":
            await self.mediaQueue.clearCommand(client, message)
        elif command == "!q" or command == "!queue":
            await self.mediaQueue.queueCommand(message)    
    

    async def reactionParser(self, command,  message):
        try:
            await globals()[command](message)
        except:
            pass 
