from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.AllianceHeaderEntry import AllianceHeaderEntry
from DB.DatabaseHandler import ClubDatabaseHandler, DatabaseHandler
from Heart.Utils.ClientsManager import ClientsManager
import json

class AllianceDataMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        db_instance = DatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(fields["AllianceID"][1])[0][1])
        db_instance.loadAccount(player, player.ID)
        allSockets = ClientsManager.GetAll()

        if player.AllianceID == fields["AllianceID"]:
            self.writeBoolean(True) # Show Online Players
        else:
            self.writeBoolean(False) # Show Online Players
        
        AllianceHeaderEntry.encode(self, clubdb_instance, clubData)

        self.writeString(clubData["Description"])

        Members = []
        for i in clubdb_instance.getMembersSorted(clubData):
            memberData = i[1]
            playerEntry = db_instance.getPlayerEntry([memberData['HighID'], memberData['LowID']])
            if playerEntry is None:
                continue
            playerData = json.loads(playerEntry[2])
            Members.append((memberData, playerData))

        self.writeVInt(len(Members))

        for memberData, playerData in Members:
            self.writeLong(memberData['HighID'], memberData['LowID'])
            self.writeVInt(memberData['Role']) # Role
            self.writeVInt(playerData['Trophies']) # Trophies
            if playerData["ID"][1] in allSockets:
                self.writeVInt(2) # Player State TODO: Members state
            else:
                self.writeVInt(0)
            self.writeVInt(1)# State Timer
            print(playerData["LastOnline"])

            highestPowerLeagueRank = 19
            self.writeVInt(highestPowerLeagueRank)
            if highestPowerLeagueRank != 0:
                self.writeVInt(19) #solo
                self.writeVInt(1) #duo

            self.writeBoolean(False) # DoNotDisturb TODO: Do not disturb sync

            self.writeString(playerData['Name']) # Player Name
            self.writeVInt(100)
            self.writeVInt(28000000 + playerData['Thumbnail']) # Player Thumbnail
            self.writeVInt(43000000 + playerData['Namecolor']) # Player Name Color
            try:
                playerData["BrawlPassActive"]
            except KeyError:
                playerData["BrawlPassActive"] = False
            if playerData["BrawlPassActive"]:
                self.writeVInt(46000000 + playerData['Namecolor']) # Color Gradients
            else:
                self.writeVInt(-1) # Color Gradients

            self.writeVInt(-1)
            self.writeBoolean(False)

            self.writeVInt(1)
            self.writeVInt(0)
            self.writeVInt(317)
            self.writeVInt(317)
            self.writeVInt(14)
            self.writeVInt(6)
            self.writeVInt(6)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(True)
            self.writeVInt(0)
            self.writeVInt(0)
            
        self.writeVInt(0)
        #self.writeVInt(0) # piggy player wins
        #self.writeVInt(0) # piggy player tickets
        #self.writeVInt(10) #
            
    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24301

    def getMessageVersion(self):
        return self.messageVersion
