from Heart.Instances.Heart.Alliance import Alliance
from Heart.Messaging import Messaging

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class RespondToAllianceJoinRequestMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["StreamID"] = self.readLong()
        fields["Accept"] = self.readBoolean()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        db_instance = DatabaseHandler()
        clubdb_instance = ClubDatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(calling_instance.player.AllianceID[1])[0][1])
        for x in clubData["ChatData"]:
        	if x['StreamID'] == fields["StreamID"]:
        		player_data = json.loads(db_instance.getPlayerEntry(x['Target']['ID'])[2])
        		if fields["Accept"]:
        			ResponseID = 90
        			x['State'] = 2
        			x['Name'] = calling_instance.player.Name
        			player_data["AllianceID"] = calling_instance.player.AllianceID
        			clubData["Members"][str(player_data["ID"][1])] = {'HighID': player_data["ID"][0], 'LowID': player_data["ID"][1], 'Name': player_data["Name"], 'Role': 1, 'Trophies': player_data["Trophies"], 'NameColor': player_data["Namecolor"], 'Thumbnail': player_data["Thumbnail"]}
        			db_instance.updatePlayer(player_data, player_data["ID"])
        		else:
        			ResponseID = 91
        			x['State'] = 3
        			x['Name'] = calling_instance.player.Name
        clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        
        allSockets = ClientsManager.GetAll()
        for x in clubData["Members"]:
        	if int(x) in allSockets:
        		fields["Socket"] = allSockets[int(x)]["Socket"]
        		Messaging.sendMessage(24312, fields, calling_instance.player)
        
        fields["Socket"] = calling_instance.client
        fields["ResponseID"] = ResponseID
        Messaging.sendMessage(24333, fields)
        fields["HasClub"] = True
        Messaging.sendMessage(24399, fields, calling_instance.player)
        Messaging.sendMessage(24311, fields, calling_instance.player)
        Messaging.sendMessage(22161, fields, calling_instance.player)

    def getMessageType(self):
        return 14321

    def getMessageVersion(self):
        return self.messageVersion