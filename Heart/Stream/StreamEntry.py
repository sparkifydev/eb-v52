from DB.DatabaseHandler import DatabaseHandler
import json


class StreamEntry:
    def encode(self, info):
        db = DatabaseHandler()
        data = json.loads(db.getPlayerEntry([info["PlayerID"][0], info["PlayerID"][1]])[2])
        self.writeVLong(info["StreamID"][0], info["StreamID"][1])
        self.writeVLong(info["PlayerID"][0], info["PlayerID"][1])
        self.writeString(data["Name"])
        self.writeVInt(info["PlayerRole"])
        self.writeVInt(0)
        self.writeVInt(0)
