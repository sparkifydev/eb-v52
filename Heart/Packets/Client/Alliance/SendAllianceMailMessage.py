from Heart.Messaging import Messaging

from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class SendAllianceMailMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        self.writeInt(0)
        self.writeString(fields["Message"])

    def decode(self):
        fields = {}
        fields["Unk"] = self.readInt()
        fields["Message"] = self.readString()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        if fields["Message"] == b'':
        	fields["Socket"] = calling_instance.client
        	fields["ResponseID"] = 114
        	Messaging.sendMessage(24333, fields)
        else:
        	db_instance = DatabaseHandler()
        	clubdb_instance = ClubDatabaseHandler()
        	player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        	clubData = json.loads(clubdb_instance.getClubWithLowID(player_data["AllianceID"][1])[0][1])
        	
        	fields["Socket"] = calling_instance.client
        	fields["ResponseID"] = 113
        	Messaging.sendMessage(24333, fields)
        	
        	fields["Notification"] = {"Type": 82, "Readed": False, "Timer": 0, "Text": fields["Message"], "Number": 0}
        	fields["Socket"] = calling_instance.client
        	fields["Command"] = {"ID": 206}
        	Messaging.sendMessage(24111, fields)


    def getMessageType(self):
        return 14330

    def getMessageVersion(self):
        return self.messageVersion