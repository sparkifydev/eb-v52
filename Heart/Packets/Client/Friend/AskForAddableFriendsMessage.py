from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging

from Heart.Record.ByteStream import ByteStream


class AskForAddableFriendsMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0
        

    def decode(self):
        fields = {}
        fields["Unk1"] = self.readVInt()
        fields["Unk2"] = self.readVInt()
        return fields

    def encode(self):
    	pass
    
    def execute(message, calling_instance, fields, cryptoInit):
        fields["Socket"] = calling_instance.client
        Messaging.sendMessage(20107, fields, cryptoInit, calling_instance.player)

    def getMessageType(self):
        return 10503

    def getMessageVersion(self):
        return self.messageVersion