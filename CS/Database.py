from CS.Character import CS_Character
import gspread
import pytz
from datetime import datetime


GMT8 = pytz.timezone('Asia/Singapore')


class CS_Database:
    def __init__(self):
        self.gc = gspread.service_account(filename='creds.json')
        self.gsheet = self.gc.open_by_key("1eN8YLqAvzYTHP3V9yv1BYV0kMKJa-FdhW-_qaj2QDJA")
        self.classes = ["Defender", "Striker", "Ranger", "Sniper", "Support", "Siege", "Tower"]
        self.data = self.getdata()
        self.charaList = self.data.keys()
        self.lastUpdated = datetime.now(GMT8).strftime('%Y-%m-%d')

    classmethod
    def getdata(self):
        data = {}
        sheet = []
        for type in self.classes:
            temp = self.gsheet.worksheet(type)
            sheet.append(temp)
        for type in sheet:
            charas = type.col_values(2)
            for i in range(len(charas)):
                rowtype = (i, type.title)
                data[charas[i]] = rowtype
        return data
    
    classmethod
    def updatedata(self):
        self.data = self.getdata()
        self.charaList = self.data.keys()
                
    classmethod
    def searchKeysByVal(self, search):
        charlist = []
        for chr in self.charaList:
            if  search.lower() in chr.lower():
                charlist.append(CS_Character(self.data[chr]))
        return charlist

    classmethod
    def charaSearch(self, search):
        if self.lastUpdated != datetime.now(GMT8).strftime('%Y-%m-%d'):
            self.updatedata()
        charlist = []
        for chr in self.charaList:
            if  search.lower() in chr.lower():
                charlist.append(CS_Character(self.data[chr], self.gsheet))
        if not charlist:
            raise Exception("Invalid search!")
        return charlist

    classmethod
    async def searchCommand(self, message):
        search = message.content[4:].lower()
        results = self.charaSearch(search)
        for chr in results:
            await message.channel.send(embed = chr.embedconstructor())
    



