from Heart.Instances.Heart.Alliance import Alliance
from Heart.Messaging import Messaging

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class LeaveAllianceMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        clubdb_instance = ClubDatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        clubEntry = clubdb_instance.getClubWithLowID(calling_instance.player.AllianceID[1])
        if not clubEntry:
            player_data["AllianceID"] = [0, 0]
            player_data["HasClub"] = False
            db_instance.updatePlayerData(player_data, calling_instance)
            fields["Socket"] = calling_instance.client
            fields["ResponseID"] = 80
            Messaging.sendMessage(24333, fields, cryptoInit, calling_instance.player)
            fields["HasClub"] = False
            Messaging.sendMessage(24399, fields, cryptoInit, calling_instance.player)
            return
        clubData = json.loads(clubEntry[0][1])
        LastMessageID = len(clubData["ChatData"])
        Role = clubData["Members"][str(player_data["ID"][1])]["Role"]
        message = {
        'StreamType': 4,
        'StreamID': [0, LastMessageID + 1],
        'PlayerID': calling_instance.player.ID,
        'PlayerName': calling_instance.player.Name,
        'PlayerRole': Role,
        'EventType': 4,
        'Target': {'ID': calling_instance.player.ID, 'Name': calling_instance.player.Name}
        }
        clubData["ChatData"].append(message)
        clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        allSockets = ClientsManager.GetAll()
        for x in clubData["Members"]:
            if int(x) in allSockets:
                fields["Socket"] = allSockets[int(x)]["Socket"]
                Messaging.sendMessage(24312, fields, cryptoInit, calling_instance.player)
        del clubData["Members"][str(calling_instance.player.ID[1])]
        if len(clubData["Members"]) == 0:
            clubdb_instance.deleteClub(calling_instance.player.AllianceID[1])
        else:
            if Role == 2:
                NewLeader = max(
                    clubData["Members"].items(),
                    key=lambda x: (x[1]["Role"], x[1]["Trophies"]),
                )
                clubData["Members"][NewLeader[0]]["Role"] = 2
            clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        
        player_data["AllianceID"] = [0, 0]
        player_data["HasClub"] = False
        db_instance.updatePlayerData(player_data, calling_instance)
        
        fields["Socket"] = calling_instance.client
        fields["ResponseID"] = 80
        Messaging.sendMessage(24333, fields, cryptoInit, calling_instance.player)
        fields["HasClub"] = False
        Messaging.sendMessage(24399, fields, cryptoInit, calling_instance.player)

    def getMessageType(self):
        return 14308

    def getMessageVersion(self):
        return self.messageVersion