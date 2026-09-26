from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler
import json


class TeamInvitationMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        db = DatabaseHandler()
        inviter = json.loads(db.getPlayerEntry(fields["InviterID"])[2])
        team = fields["TeamID"]

        self.writeVInt(1)
        self.writeLong(team[0], team[1])
        self.writeLong(fields["InviterID"][0], fields["InviterID"][1])
        self.writeString(inviter["Name"])
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeInt(inviter["Trophies"])
        self.writeInt(1)
        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)
        self.writeBoolean(False)
        self.writeString()
        self.writeInt(0)
        self.writeInt(0)
        self.writeBoolean(True)
        self.writeString(inviter["Name"])
        self.writeVInt(0)
        self.writeVInt(28000000 + inviter["Thumbnail"])
        self.writeVInt(43000000 + inviter["Namecolor"])
        self.writeVInt(-1)
        self.writeInt(0)
        self.writeInt(0)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24589

    def getMessageVersion(self):
        return self.messageVersion
