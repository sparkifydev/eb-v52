from Heart.Packets.PiranhaMessage import PiranhaMessage


class FriendLoggedOutMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player=None):
        self.writeLong(fields["IDHigh"], fields["IDLow"])

    def decode(self):
        return {}

    def execute(self, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20111

    def getMessageVersion(self):
        return self.messageVersion
