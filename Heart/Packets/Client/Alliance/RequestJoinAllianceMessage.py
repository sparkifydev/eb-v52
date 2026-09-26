from Heart.Instances.Heart.Alliance import Alliance
from Heart.Messaging import Messaging

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class RequestJoinAllianceMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["AllianceID"] = self.readLong()
        fields["Message"] = self.readString()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        db_instance = DatabaseHandler()
        clubdb_instance = ClubDatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        clubData = json.loads(clubdb_instance.getClubWithLowID(fields["AllianceID"][1])[0][1])
        LastMessageID = len(clubData["ChatData"])
        message = {
        'StreamType': 3,
        'StreamID': [0, LastMessageID + 1],
        'PlayerID': calling_instance.player.ID,
        'PlayerName': calling_instance.player.Name,
        'PlayerRole': 1,
        'Target': {'ID': calling_instance.player.ID},
        'Message': fields["Message"],
        'Name': "",
        'State': 1
        }
        clubData["ChatData"].append(message)
        clubdb_instance.updateClubData(clubData, fields["AllianceID"][1])
        allSockets = ClientsManager.GetAll()
        for x in clubData["Members"]:
        	if int(x) in allSockets:
        		fields["Socket"] = allSockets[int(x)]["Socket"]
        		Messaging.sendMessage(24312, fields, calling_instance.player)
        
        fields["Socket"] = calling_instance.client
        fields["ResponseID"] = 50
        Messaging.sendMessage(24333, fields)

    def getMessageType(self):
        return 14317

    def getMessageVersion(self):
        return self.messageVersion