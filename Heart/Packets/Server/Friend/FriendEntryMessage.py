from Heart.Record.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler


class FriendEntryMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        self.writeBoolean(fields["IsOnline"])

        friend = fields["Friend"]
        self.writeString(friend["Name"])
        self.writeInt(friend["Trophies"])
        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)
        self.writeLong(friend["IDHigh"], friend["IDLow"])
        self.writeLong(0, 0)
        self.writeLong(0, 0)
        self.writeLong(0, 0)
        self.writeLong(0, 0)
        self.writeBoolean(False)
        self.writeInt(0)
        self.writeLong(0, 0)
        has = "Thumbnail" in friend
        self.writeBoolean(has)
        if has:
            self.writeString(friend["Name"])
            self.writeVInt(friend["Thumbnail"])
            self.writeVInt(friend["NameColor"])
            self.writeVInt(0)
            self.writeVInt(-1)
        self.writeLong(0, 0)
        self.writeLong(0, 0)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields, cryptoInit):
        pass

    def getMessageType(self):
        return 20106

    def getMessageVersion(self):
        return self.messageVersion
