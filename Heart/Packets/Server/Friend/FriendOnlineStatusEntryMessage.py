from Heart.Packets.PiranhaMessage import PiranhaMessage


class FriendOnlineStatusEntryMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player=None):
        self.writeLong(fields["AccountIDHigh"], fields["AccountIDLow"])
        self.writeBoolean(fields["IsOnline"])
        if fields["IsOnline"]:
            self.writeLong(fields["AccountIDHigh"], fields["AccountIDLow"])
            self.writeVInt(fields["Status"])
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeBoolean(False)

    def decode(self):
        return {}

    def execute(self, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24555

    def getMessageVersion(self):
        return self.messageVersion
