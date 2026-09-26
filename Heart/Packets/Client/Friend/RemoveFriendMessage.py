from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import DatabaseHandler
import json


class RemoveFriendMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def decode(self):
        fields = {}
        fields["AccountID"] = self.readLong()
        super().decode(fields)
        return fields

    def encode(self, fields):
        pass

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        sockets = ClientsManager.GetAll()

        targetID  = fields["AccountID"]
        targetLow = targetID[1]
        selfID    = calling_instance.player.ID

        db.DelFriend(selfID[1], targetLow)
        db.DelFriend(targetLow, selfID[1])

        tentry = db.getPlayerEntry(targetID)
        tdata  = json.loads(tentry[2]) if tentry is not None else None

        selfEntry = db.getPlayerEntry(selfID)
        selfData  = json.loads(selfEntry[2]) if selfEntry is not None else None

        if tdata is not None:
            Messaging.sendMessage(20106, {
                "Socket":   calling_instance.client,
                "IsOnline": False,
                "Friend": {
                    "IDHigh":      targetID[0],
                    "IDLow":       targetID[1],
                    "Name":        tdata["Name"],
                    "Trophies":    tdata["Trophies"],
                    "Thumbnail":   tdata["Thumbnail"],
                    "NameColor":   tdata["Namecolor"],
                    "FriendState": 0,
                    "LastOnline": 0,
                },
            }, cryptoInit, calling_instance.player)

        if targetLow in sockets and selfData is not None:
            entry = sockets[targetLow]
            Messaging.sendMessage(20106, {
                "Socket":   entry["Socket"],
                "IsOnline": False,
                "Friend": {
                    "IDHigh":      selfID[0],
                    "IDLow":       selfID[1],
                    "Name":        selfData["Name"],
                    "Trophies":    selfData["Trophies"],
                    "Thumbnail":   selfData["Thumbnail"],
                    "NameColor":   selfData["Namecolor"],
                    "FriendState": 0,
                    "LastOnline": 0,
                },
            }, entry["CryptoInit"], calling_instance.player)

    def getMessageType(self):
        return 10506

    def getMessageVersion(self):
        return self.messageVersion
