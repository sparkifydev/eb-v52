import json

from Heart.Messaging import Messaging
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Utils.Friend import iFriends, nOnline, nFriends
from DB.DatabaseHandler import DatabaseHandler


class LoginMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["AccountID"]                 = self.readLong()
        fields["PassToken"]                 = self.readString()
        fields["ClientMajor"]               = self.readInt()
        fields["ClientMinor"]               = self.readInt()
        fields["ClientBuild"]               = self.readInt()
        fields["ResourceSha"]               = self.readString()
        fields["Device"]                    = self.readString()
        fields["PreferredLanguage"]         = self.readDataReference()
        fields["PreferredDeviceLanguage"]   = self.readString()
        fields["OSVersion"]                 = self.readString()
        fields["isAndroid"]                 = self.readBoolean()
        fields["IMEI"]                      = self.readString()
        fields["AndroidID"]                 = self.readString()
        fields["isAdvertisingEnabled"]      = self.readBoolean()
        fields["AppleIFV"]                  = self.readString()
        fields["RndKey"]                    = self.readInt()
        fields["AppStore"]                  = self.readVInt()
        fields["ClientVersion"]             = self.readString()
        fields["TencentOpenId"]             = self.readString()
        fields["TencentToken"]              = self.readString()
        fields["TencentPlatform"]           = self.readVInt()
        fields["DeviceVerifierResponse"]    = self.readString()
        fields["AppLicensingSignature"]     = self.readString()
        fields["DeviceVerifierResponse"]    = self.readString()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        if fields["ClientMajor"] != 52:
            return

        calling_instance.player.ClientVersion = (
            f'{fields["ClientMajor"]}.{fields["ClientBuild"]}.{fields["ClientMinor"]}'
        )
        fields["Socket"] = calling_instance.client

        db_instance = DatabaseHandler()
        if db_instance.playerExist(fields["PassToken"], fields["AccountID"]):
            player_data = json.loads(db_instance.getPlayerEntry(fields["AccountID"])[2])
            db_instance.loadAccount(calling_instance.player, fields["AccountID"])
        else:
            player_data = calling_instance.player.getDataTemplate(
                fields["AccountID"][0], fields["AccountID"][1], fields["PassToken"]
            )
            db_instance.createAccount(player_data)

        ClientsManager.AddPlayer(calling_instance.player.ID, calling_instance.client, cryptoInit)

        Messaging.sendMessage(20104, fields, cryptoInit, calling_instance.player)
        Messaging.sendMessage(24101, fields, cryptoInit, calling_instance.player)
        Messaging.sendMessage(24399, fields, cryptoInit, calling_instance.player)
        fields["Command"] = {"ID": 221}
        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)

        if player_data["HasClub"]:
            Messaging.sendMessage(24311, fields, cryptoInit, calling_instance.player)

        if player_data["TeamID"] != [0, 0]:
            from DB.DatabaseHandler import TeamDatabaseHandler
            td = TeamDatabaseHandler()
            team_row = td.getTeamWithLowID(player_data["TeamID"][1])
            if team_row:
                Messaging.sendMessage(24124, fields, cryptoInit, calling_instance.player)
            else:
                player_data["TeamID"] = [0, 0]
                db_instance.updatePlayerData(player_data, calling_instance)

        fields["Friends"] = iFriends(player_data)
        print(fields["Friends"])
        Messaging.sendMessage(20105, fields, cryptoInit, calling_instance.player)

        nOnline(calling_instance.player.ID, player_data)
        nFriends(calling_instance.player.ID, player_data)

    def getMessageType(self):
        return 10101

    def getMessageVersion(self):
        return self.messageVersion
