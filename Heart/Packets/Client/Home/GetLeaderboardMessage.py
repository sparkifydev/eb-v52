from Heart.Messaging import Messaging
from Heart.Packets.PiranhaMessage import PiranhaMessage


class GetLeaderboardMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["IsRegional"] = self.readBoolean()
        fields["LeaderboardType"] = self.readVInt()
        fields["HeroDataID"] = self.readDataReference()
        fields["RegionID"] = self.readVInt()
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        fields["Socket"] = calling_instance.client
        Messaging.sendMessage(24403, fields, cryptoInit, calling_instance.player)

    def getMessageType(self):
        return 14403

    def getMessageVersion(self):
        return self.messageVersion
