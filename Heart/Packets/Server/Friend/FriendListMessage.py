from Heart.Packets.PiranhaMessage import PiranhaMessage


class FriendListMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        friends = fields["Friends"]

        self.writeInt(0)
        self.writeBoolean(True)
        self.writeBoolean(False)
        self.writeInt(len(friends))

        for friend in friends:
            self.writeLong(friend["IDHigh"], friend["IDLow"])

            self.writeString(friend["Name"])
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()

            self.writeInt(friend["Trophies"])
            self.writeInt(friend["FriendState"])
            self.writeInt(0)
            self.writeInt(0)
            self.writeInt(0)

            self.writeBoolean(False)
            self.writeString()
            self.writeInt(friend["LastOnline"])
            self.writeInt(19)

            self.writeBoolean(True)
            self.writeString(friend["Name"])
            self.writeVInt(5000)
            self.writeVInt(28000000 + friend["Thumbnail"])
            self.writeVInt(43000000 + friend["NameColor"])
            self.writeVInt(-1)

            self.writeInt(0)
            self.writeInt(0)

    def decode(self):
        return {}

    def execute(self, message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20105

    def getMessageVersion(self):
        return self.messageVersion
