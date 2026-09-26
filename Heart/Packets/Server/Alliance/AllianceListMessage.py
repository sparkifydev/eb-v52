from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import ClubDatabaseHandler
from Heart.Utils.AllianceHeaderEntry import AllianceHeaderEntry
import random

class AllianceListMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        allClubs = clubdb_instance.getAllClub()
        finalList = []

        found = 0
        for i in allClubs:
        	if found == 100:
        		return
        	elif i["Name"].lower().startswith(fields["SearchString"]):
        		finalList.append(i)
        		found += 1
        
        self.writeString(fields["SearchString"])
        
        self.writeVInt(len(finalList))

        for clubData in finalList:
            AllianceHeaderEntry.encode(self, clubdb_instance, clubData)

    def decode(self):
        return { }

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24310

    def getMessageVersion(self):
        return self.messageVersion