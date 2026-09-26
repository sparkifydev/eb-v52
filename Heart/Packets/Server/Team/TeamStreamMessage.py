from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import TeamDatabaseHandler
from Heart.Stream.StreamEntryFactory import StreamEntryFactory
import json


class TeamStreamMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        td = TeamDatabaseHandler()
        if not player.TeamID or player.TeamID == [0, 0]:
            self.writeVLong(0, 0)
            self.writeVInt(0)
            return
        row = td.getTeamWithLowID(player.TeamID[1])
        if not row:
            self.writeVLong(0, 0)
            self.writeVInt(0)
            return
        team = json.loads(row[0][1])
        chat = team["ChatData"] if "ChatData" in team else []
        if not isinstance(chat, list):
            chat = []
        self.writeVLong(team["HighID"], team["LowID"])
        self.writeVInt(len(chat))
        for entry in chat:
            self.writeVInt(entry["StreamType"])
            StreamEntryFactory.encode(self, fields, entry)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24131

    def getMessageVersion(self):
        return self.messageVersion
