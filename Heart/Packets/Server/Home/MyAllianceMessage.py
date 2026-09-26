from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.AllianceHeaderEntry import AllianceHeaderEntry
from DB.DatabaseHandler import ClubDatabaseHandler, DatabaseHandler
from Heart.Utils.ClientsManager import ClientsManager
import json
from Heart.Messaging import Messaging

class MyAllianceMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        if player.HasClub == True:
            print(player.HasClub)
            db_instance = DatabaseHandler()
            clubdb_instance = ClubDatabaseHandler()
            clubData = json.loads(clubdb_instance.getClubWithLowID(player.AllianceID[1])[0][1])
            localMemberData = clubdb_instance.getMemberWithLowID(clubData, player.ID[1])
            allSockets = ClientsManager.GetAll()

            OnlineMembers = 0
            for i in clubdb_instance.getMembersSorted(clubData):
                memberData = i[1]
                playerData = json.loads(db_instance.getPlayerEntry([memberData['HighID'], memberData['LowID']])[2])
                if playerData["ID"][1] in allSockets:
                    OnlineMembers += 1
            self.writeVInt(OnlineMembers) # Onlines Members TODO: members state
            self.writeBoolean(True)
            self.writeDataReference(25, localMemberData["Role"])
        
            AllianceHeaderEntry.encode(self, clubdb_instance, clubData)

            self.writeBoolean(False)
        else:
            self.writeVInt(0)
            self.writeVInt(0)

    def decode(self):
        fields = {}
        fields["ResponseID"] = self.readVInt()
        fields["Unk1"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24399

    def getMessageVersion(self):
        return self.messageVersion