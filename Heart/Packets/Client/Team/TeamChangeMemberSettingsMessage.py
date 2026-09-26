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
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        sid = fields["Skin"][1] if fields["Skin"][1] else 0
        bid = pd["SelectedBrawler"]
        pd["SelectedSkins"][str(bid)] = sid
        db.updatePlayerData(pd, calling_instance)
        team = json.loads(td.getTeamWithLowID(calling_instance.player.TeamID[1])[0][1])
        low = str(calling_instance.player.ID[1])
        member = team["Members"][low]
        member["Status"] = 3
        if "Brawler" in member and member["Brawler"]:
            member["Skin"] = [29, sid] if sid > 0 else [0, 0]
        td.updateTeamData(team, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for low in team["Members"]:
            socket_id = int(low)
            if socket_id in sockets:
                fields["Socket"] = sockets[socket_id]["Socket"]
                Messaging.sendMessage(24124, fields, sockets[socket_id]["CryptoInit"], calling_instance.player)
        team = json.loads(td.getTeamWithLowID(calling_instance.player.TeamID[1])[0][1])
        low = str(calling_instance.player.ID[1])
        member = team["Members"][low]
        member["Status"] = 3
        member["Skin"] = [29, sid] if sid > 0 else [0, 0]
        td.updateTeamData(team, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for low in team["Members"]:
            socket_id = int(low)
            if socket_id in sockets:
                fields["Socket"] = sockets[socket_id]["Socket"]
                Messaging.sendMessage(24124, fields, sockets[socket_id]["CryptoInit"], calling_instance.player)

    def getMessageType(self):
        return 14354

    def getMessageVersion(self):
        return self.messageVersion
