from Heart.Record.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler


class AddableFriendsMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0
        

    def encode(self, fields):
        self.writeInt(1)
        
        self.writeInt(1)
        self.writeInt(2)
        self.writeString("KulerDick")
        self.writeInt(0)
        self.writeString("KulerDick")


    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20107

    def getMessageVersion(self):
        return self.messageVersion
