from Heart.Messaging import Messaging

from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import random
import json


class ChatToAllianceStreamMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["Message"] = self.readString()
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        clubdb_instance = ClubDatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(calling_instance.player.AllianceID[1])[0][1])
        
        commands = ["./clearallchatdata", "./clearteams"]
        if fields["Message"] == "./clearallchatdata":
        	allClubs = clubdb_instance.getAllClub()
        	for club_Data in allClubs:
        		club_Data["ChatData"] = []
        		clubdb_instance.updateClubData(club_Data, club_Data["LowID"])
        
        if fields["Message"] == "./clearteams":
        	allplayers = db_instance.load_all()
        	for player_Data in allplayers:
        		player_Data["TeamID"] = [0, 0]
        		db_instance.updatePlayer(player_Data, player_Data["ID"])
        
        
        if fields["Message"] not in commands:
        	LastMessageID = len(clubData["ChatData"])
        	Role = clubData["Members"][str(playerData["ID"][1])]["Role"]
        	message = {
        	'StreamType': 2,
        	'StreamID': [0, LastMessageID + 1],
        	'PlayerID': calling_instance.player.ID,
        	'PlayerName': calling_instance.player.Name,
        	'PlayerRole': Role,
        	'Message': fields["Message"]
        	}
        	clubData["ChatData"].append(message)
        	clubdb_instance.updateClubData(clubData, calling_instance.player.AllianceID[1])
        	allSockets = ClientsManager.GetAll()
        	for x in clubData["Members"]:
        		if int(x) in allSockets:
        			fields["Socket"] = allSockets[int(x)]["Socket"]
        			Messaging.sendMessage(24312, fields, cryptoInit, calling_instance.player)


    def getMessageType(self):
        return 14315

    def getMessageVersion(self):
        return self.messageVersion