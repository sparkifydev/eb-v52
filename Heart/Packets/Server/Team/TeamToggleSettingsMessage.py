from Heart.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging


class TeamToggleSettingsMessage(PiranhaMessage):


    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0


    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        return fields


    def execute(message, calling_instance, fields):
        pass


    def getMessageType(self):
        return 14372


    def getMessageVersion(self):
        return self.messageVersion
