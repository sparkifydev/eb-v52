import json

from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from Heart.Utils.Friend import iFriends
from DB.DatabaseHandler import DatabaseHandler


class AskForFriendListMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def decode(self):
        return {}

    def encode(self):
        pass

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        pentry = db.getPlayerEntry(calling_instance.player.ID)
        if pentry is None:
            return
        pdata = json.loads(pentry[2])

        fields["Socket"]   = calling_instance.client
        fields["Friends"]  = iFriends(pdata)
        Messaging.sendMessage(20105, fields, cryptoInit, calling_instance.player)

    def getMessageType(self):
        return 10504

    def getMessageVersion(self):
        return self.messageVersion
