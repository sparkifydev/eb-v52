from Heart.Packets.PiranhaMessage import PiranhaMessage


class TeamSetMemberReadyMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Ready"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 14355

    def getMessageVersion(self):
        return self.messageVersion
