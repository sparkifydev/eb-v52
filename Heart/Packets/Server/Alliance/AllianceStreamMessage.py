from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import ClubDatabaseHandler
from Heart.Stream.StreamEntryFactory import StreamEntryFactory
import json

class AllianceStreamMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(player.AllianceID[1])[0][1])

        if len(clubData["ChatData"]) >= 100:
        	self.writeVInt(100)
        else:
        	self.writeVInt(len(clubData["ChatData"]))
        for i in clubData['ChatData']:
            if len(clubData["ChatData"]) >= 100:
            	if clubData['ChatData'].index(i) >= len(clubData['ChatData']) - 100:
            		self.writeVInt(i['StreamType'])
            		StreamEntryFactory.encode(self, fields, i)
            else:
            	self.writeVInt(i['StreamType'])
            	StreamEntryFactory.encode(self, fields, i)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24311

    def getMessageVersion(self):
        return self.messageVersion