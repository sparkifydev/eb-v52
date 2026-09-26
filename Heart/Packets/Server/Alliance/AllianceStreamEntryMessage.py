from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import ClubDatabaseHandler
from Heart.Stream.StreamEntryFactory import StreamEntryFactory
import json

class AllianceStreamEntryMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        clubdb_instance = ClubDatabaseHandler()
        clubData = json.loads(clubdb_instance.getClubWithLowID(player.AllianceID[1])[0][1])

        StreamID = len(clubData["ChatData"])
        for i in clubData['ChatData']:
            if i['StreamID'][1] == StreamID:
            	self.writeVInt(i['StreamType'])
            	StreamEntryFactory.encode(self, fields, i)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24312

    def getMessageVersion(self):
        return self.messageVersion