from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Messaging import Messaging
import json


class TeamChangeMemberSettingsMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Brawler"] = self.readDataReference()
        fields["Skin"] = self.readDataReference()
        fields["Unk1"] = self.readVInt()
        fields["Unk2"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        td = TeamDatabaseHandler()
        db = DatabaseHandler()
        p = calling_instance.player
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        print("hi1:", pd["SelectedSkin"])
        bid = p.SelectedBrawler
        sid = p.SelectedSkin
        pd["SelectedSkin"] = sid
        print("hi2:", pd["SelectedSkin"])
        db.updatePlayerData(pd, calling_instance)
        team = json.loads(td.getTeamWithLowID(p.TeamID[1])[0][1])
        low = str(p.ID[1])
        member = team["Members"][low]
        member["Status"] = 3
        member["Brawler"] = [29, bid]
        member["Skin"] = [29, sid] if sid > 0 else [0, 0]
        td.updateTeamData(team, p.TeamID[1])
        fields["Brawler"] = [29, bid]
        fields["Skin"] = [29, sid] if sid > 0 else [0, 0]
        sockets = ClientsManager.GetAll()
        for low in team["Members"]:
            if int(low) in sockets:
                fields["Socket"] = sockets[int(low)]["Socket"]
                Messaging.sendMessage(24124, fields, sockets[int(low)]["CryptoInit"], p)

    def getMessageType(self):
        return 14354

    def getMessageVersion(self):
        return self.messageVersion
