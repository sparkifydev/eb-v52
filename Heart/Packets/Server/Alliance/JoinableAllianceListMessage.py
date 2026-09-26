from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import ClubDatabaseHandler, DatabaseHandler
from Heart.Utils.AllianceHeaderEntry import AllianceHeaderEntry
import random

class JoinableAllianceListMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        db_instance = DatabaseHandler()
        allClubs = []
        for clubData in clubdb_instance.getAllClub():
            if len(clubData["Members"]) == 0:
                continue
            for i in clubData["Members"].values():
                if db_instance.getPlayerEntry([i["HighID"], i["LowID"]]) is not None:
                    allClubs.append(clubData)
                    break

        if len(allClubs) >= 50:
            maxClub = 50
            self.writeVInt(50)
        elif len(allClubs) == 0:
            maxClub = -1
            self.writeVInt(0)
        else:
            maxClub = len(allClubs)
            self.writeVInt(len(allClubs))


        if maxClub > 1:
            found = 0
            randomClubList = []
            while found != maxClub:
                randomEntry = random.choice(allClubs)
                if randomEntry not in randomClubList:
                    randomClubList.append(randomEntry)
                    found += 1

        for clubData in allClubs:
            AllianceHeaderEntry.encode(self, clubdb_instance, clubData)

    def decode(self):
        return { }

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24304

    def getMessageVersion(self):
        return self.messageVersion