from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry
from DB.DatabaseHandler import DatabaseHandler
import json


class AllianceEventStreamEntry:
    def encode(self: ByteStream, info):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry([info['Target']['ID'][0], info['Target']['ID'][1]])[2])
        
        StreamEntry.encode(self, info)
        self.writeVInt(info['EventType'])
        self.writeBoolean(info['Target'] != {})
        if info['Target'] != {}:
            self.writeVLong(info['Target']['ID'][0], info['Target']['ID'][1])
            self.writeString(playerData['Name'])

