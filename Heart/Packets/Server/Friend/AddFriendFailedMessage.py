from Heart.Record.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler


class AddFriendFailedMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        self.writeInt(fields["ErrorCode"])

    def decode(self):
        return {}

    def execute(message, calling_instance, fields, cryptoInit):
        pass

    def getMessageType(self):
        return 20112

    def getMessageVersion(self):
        return self.messageVersion
