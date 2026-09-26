from Heart.Instances.Heart.Alliance import Alliance
from Heart.Messaging import Messaging

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class KickAllianceMemberMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["PlayerID"] = self.readLong()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        db_instance = DatabaseHandler()
        clubdb_instance = ClubDatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(fields["PlayerID"])[2])
        clubData = json.loads(clubdb_instance.getClubWithLowID(calling_instance.player.AllianceID[1])[0][1])
        
        LastMessageID = len(clubData["ChatData"])
        Role = clubData["Members"][str(calling_instance.player.ID[1])]["Role"]
        message = {
        'StreamType': 4,
        'StreamID': [0, LastMessageID + 1],
        'PlayerID': calling_instance.player.ID,
        'PlayerName': calling_instance.player.Name,
        'PlayerRole': Role,
        'EventType': 1,
        'Target': {'ID': player_data["ID"], 'Name': player_data["Name"]}
        }
        clubData["ChatData"].append(message)
        del clubData["Members"][str(fields["PlayerID"][1])]
        clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        player_data["AllianceID"] = [0, 0]
        db_instance.updatePlayer(player_data, player_data["ID"])
        allSockets = ClientsManager.GetAll()
        for x in clubData["Members"]:
        	if int(x) in allSockets:
        		fields["Socket"] = allSockets[int(x)]["Socket"]
        		Messaging.sendMessage(24312, fields, calling_instance.player)
        
        fields["Socket"] = calling_instance.client
        fields["ResponseID"] = 70
        Messaging.sendMessage(24333, fields)
        fields["HasClub"] = True
        Messaging.sendMessage(24399, fields, calling_instance.player)
        Messaging.sendMessage(24311, fields, calling_instance.player)

    def getMessageType(self):
        return 14307

    def getMessageVersion(self):
        return self.messageVersion