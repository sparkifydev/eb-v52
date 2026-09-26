from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry
from Heart.Utils.PlayerDisplayData import PlayerDisplayData
from DB.DatabaseHandler import DatabaseHandler
import json


class JoinRequestAllianceStreamEntry:
    def encode(self: ByteStream, info):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry([info['PlayerID'][0], info['PlayerID'][1]])[2])
        
        StreamEntry.encode(self, info)
        self.writeString(info['Message'])
        self.writeString(playerData['Name'])
        self.writeVInt(info['State'])
        PlayerDisplayData.encode(self, info['Target'])

