import json

from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import DatabaseHandler


class AddFriendMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def decode(self):
        fields = {}
        fields["AccountID"] = self.readLong()
        fields["Mode"]      = self.readInt()
        fields["Unk"]       = self.readInt()
        super().decode(fields)
        return fields

    def encode(self, fields):
        pass

    def execute(message, calling_instance, fields, cryptoInit):
        db         = DatabaseHandler()
        sockets = ClientsManager.GetAll()

        targetID  = fields["AccountID"]
        targetLow = targetID[1]
        selfID    = calling_instance.player.ID

        tentry = db.getPlayerEntry(targetID)
        if tentry is None:
            fields["Socket"]    = calling_instance.client
            fields["ErrorCode"] = 1
            Messaging.sendMessage(20112, fields, cryptoInit, calling_instance.player)
            return

        tdata  = json.loads(tentry[2])
        centry = db.getPlayerEntry(selfID)
        cdata  = json.loads(centry[2])

        mode = fields["Mode"]

        if mode == 0:
            db.AddFriend(selfID[1], targetLow, 2)
            db.AddFriend(targetLow, selfID[1], 3)

            Messaging.sendMessage(20106, {
                "Socket":   calling_instance.client,
                "IsOnline": targetLow in sockets,
                "Friend": {
                    "IDHigh":      targetID[0],
                    "IDLow":       targetID[1],
                    "Name":        tdata["Name"],
                    "Trophies":    tdata["Trophies"],
                    "Thumbnail":   tdata["Thumbnail"],
                    "NameColor":   tdata["Namecolor"],
                    "FriendState": 2,
                    "LastOnline": 0,
                },
            }, cryptoInit, calling_instance.player)

            if targetLow in sockets:
                entry = sockets[targetLow]
                Messaging.sendMessage(20106, {
                    "Socket":   entry["Socket"],
                    "IsOnline": True,
                    "Friend": {
                        "IDHigh":      selfID[0],
                        "IDLow":       selfID[1],
                        "Name":        cdata["Name"],
                        "Trophies":    cdata["Trophies"],
                        "Thumbnail":   cdata["Thumbnail"],
                        "NameColor":   cdata["Namecolor"],
                        "FriendState": 3,
                        "LastOnline": 0,
                    },
                }, entry["CryptoInit"], calling_instance.player)

        elif mode == 4:
            db.AddFriend(selfID[1], targetLow, 4)
            db.AddFriend(targetLow, selfID[1], 4)

            online = targetLow in sockets

            Messaging.sendMessage(20106, {
                "Socket":   calling_instance.client,
                "IsOnline": online,
                "Friend": {
                    "IDHigh":      targetID[0],
                    "IDLow":       targetID[1],
                    "Name":        tdata["Name"],
                    "Trophies":    tdata["Trophies"],
                    "Thumbnail":   tdata["Thumbnail"],
                    "NameColor":   tdata["Namecolor"],
                    "FriendState": 4,
                    "LastOnline": 0,
                },
            }, cryptoInit, calling_instance.player)

            if online:
                entry = sockets[targetLow]
                Messaging.sendMessage(20106, {
                    "Socket":   entry["Socket"],
                    "IsOnline": True,
                    "Friend": {
                        "IDHigh":      selfID[0],
                        "IDLow":       selfID[1],
                        "Name":        cdata["Name"],
                        "Trophies":    cdata["Trophies"],
                        "Thumbnail":   cdata["Thumbnail"],
                        "NameColor":   cdata["Namecolor"],
                        "FriendState": 4,
                        "LastOnline": 0,
                    },
                }, entry["CryptoInit"], calling_instance.player)
        #add friend from clubb
        elif mode == 1:
            db.AddFriend(selfID[1], targetLow, 2)
            db.AddFriend(targetLow, selfID[1], 3)

            Messaging.sendMessage(20106, {
                "Socket":   calling_instance.client,
                "IsOnline": targetLow in sockets,
                "Friend": {
                    "IDHigh":      targetID[0],
                    "IDLow":       targetID[1],
                    "Name":        tdata["Name"],
                    "Trophies":    tdata["Trophies"],
                    "Thumbnail":   tdata["Thumbnail"],
                    "NameColor":   tdata["Namecolor"],
                    "FriendState": 2,
                    "LastOnline": 0,
                },
            }, cryptoInit, calling_instance.player)

            if targetLow in sockets:
                entry = sockets[targetLow]
                Messaging.sendMessage(20106, {
                    "Socket":   entry["Socket"],
                    "IsOnline": True,
                    "Friend": {
                        "IDHigh":      selfID[0],
                        "IDLow":       selfID[1],
                        "Name":        cdata["Name"],
                        "Trophies":    cdata["Trophies"],
                        "Thumbnail":   cdata["Thumbnail"],
                        "NameColor":   cdata["Namecolor"],
                        "FriendState": 3,
                        "LastOnline": 0,
                    },
                }, entry["CryptoInit"], calling_instance.player)    
#я думаю это для добавления друга с тимы, если 0 по тегу, 1 с клуба, 2/3 с тимы, 4 принять, если не так  -- поменяйье!
#я не стал проверять добавление с тимы, поэтому это за вами!!!!!
        elif mode == 2:
            db.AddFriend(selfID[1], targetLow, 2)
            db.AddFriend(targetLow, selfID[1], 3)

            Messaging.sendMessage(20106, {
                "Socket":   calling_instance.client,
                "IsOnline": targetLow in sockets,
                "Friend": {
                    "IDHigh":      targetID[0],
                    "IDLow":       targetID[1],
                    "Name":        tdata["Name"],
                    "Trophies":    tdata["Trophies"],
                    "Thumbnail":   tdata["Thumbnail"],
                    "NameColor":   tdata["Namecolor"],
                    "FriendState": 2,
                    "LastOnline": 0,
                },
            }, cryptoInit, calling_instance.player)

            if targetLow in sockets:
                entry = sockets[targetLow]
                Messaging.sendMessage(20106, {
                    "Socket":   entry["Socket"],
                    "IsOnline": True,
                    "Friend": {
                        "IDHigh":      selfID[0],
                        "IDLow":       selfID[1],
                        "Name":        cdata["Name"],
                        "Trophies":    cdata["Trophies"],
                        "Thumbnail":   cdata["Thumbnail"],
                        "NameColor":   cdata["Namecolor"],
                        "FriendState": 3,
                        "LastOnline": 0,
                    },
                }, entry["CryptoInit"], calling_instance.player)    

    def getMessageType(self):
        return 10502

    def getMessageVersion(self):
        return self.messageVersion
