from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import TeamDatabaseHandler, DatabaseHandler
import json


class TeamGameStartingMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        td = TeamDatabaseHandler()
        db = DatabaseHandler()
        teamData = json.loads(td.getTeamWithLowID(player.TeamID[1])[0][1])
        
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)


    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24130

    def getMessageVersion(self):
        return self.messageVersion