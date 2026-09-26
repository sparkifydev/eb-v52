from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.AllianceHeaderEntry import AllianceHeaderEntry
from DB.DatabaseHandler import ClubDatabaseHandler, DatabaseHandler
from Heart.Utils.ClientsManager import ClientsManager
import json

class AllianceOnlineStatusUpdatedMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        db_instance = DatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(player.AllianceID[1])[0][1])
        db_instance.loadAccount(player, player.ID)
        allSockets = ClientsManager.GetAll()

        self.writeVInt(1)
        self.writeVInt(1) #Count
        for i in range(1):
            self.writeVLong(8, 43928836) # PlayerID
            self.writeVInt(2)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20207

    def getMessageVersion(self):
        return self.messageVersion
