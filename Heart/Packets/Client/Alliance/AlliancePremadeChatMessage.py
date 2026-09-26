from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import random
import json


class AlliancePremadeChatMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass
        
    def decode(self):
        fields = {}
        fields["Unk1"] = self.readVInt()
        fields["MessageDataID"] = self.readVInt()
        fields["EmoteID"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        clubdb_instance = ClubDatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(calling_instance.player.AllianceID[1])[0][1])
        
        LastMessageID = len(clubData["ChatData"])
        Role = clubData["Members"][str(playerData["ID"][1])]["Role"]
        message = {
        'StreamType': 8,
        'StreamID': [0, LastMessageID + 1],
        'PlayerID': calling_instance.player.ID,
        'PlayerName': calling_instance.player.Name,
        'PlayerRole': Role,
        'MessageDataID': fields["MessageDataID"],
        'PremadeID': fields["EmoteID"]
        }
        clubData["ChatData"].append(message)
        clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        allSockets = ClientsManager.GetAll()
        for x in clubData["Members"]:
        	if int(x) in allSockets:
        		fields["Socket"] = allSockets[int(x)]["Socket"]
        		Messaging.sendMessage(24312, fields, cryptoInit, calling_instance.player)
        

    def getMessageType(self):
        return 14469

    def getMessageVersion(self):
        return self.messageVersion