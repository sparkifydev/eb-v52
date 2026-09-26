from Heart.Packets.PiranhaMessage import PiranhaMessage


class FriendOnlineStatusMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player=None):
        self.writeLong(fields["IDHigh"], fields["IDLow"])
        self.writeBoolean(fields["IsOnline"])
        self.writeInt(0)    # Status: 0 = в меню

    def decode(self):
        return {}

    def execute(self, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20109

    def getMessageVersion(self):
        return self.messageVersion
