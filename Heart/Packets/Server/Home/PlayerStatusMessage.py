from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage


class PlayerStatusMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Status"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        from Heart.Utils.Friend import sOnline

        allSockets = ClientsManager.GetAll()
        if calling_instance.player.ID[1] not in allSockets:
            return

        status = fields["Status"]
        calling_instance.player.PlayerStatus = status
        allSockets[calling_instance.player.ID[1]]["PlayerStatus"] = status

        for friendRef in calling_instance.player.Friends:
            if friendRef["Status"] != 4:
                continue
            friendLow = friendRef["IDLow"]
            if friendLow in allSockets:
                sOnline(
                    allSockets[friendLow],
                    calling_instance.player.ID[0],
                    calling_instance.player.ID[1],
                    status,
                )

    def getMessageType(self):
        return 14366

    def getMessageVersion(self):
        return self.messageVersion
