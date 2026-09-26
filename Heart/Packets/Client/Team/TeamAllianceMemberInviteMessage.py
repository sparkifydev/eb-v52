from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
from Heart.Messaging import Messaging
import json


class TeamAllianceMemberInviteMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["PlayerIDHigh"] = self.readVInt()
        fields["PlayerIDLow"] = self.readVInt()
        fields["Side"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        row = td.getTeamWithLowID(calling_instance.player.TeamID[1])
        if not row:
            return
        team = json.loads(row[0][1])
        targetID = [fields["PlayerIDHigh"], fields["PlayerIDLow"]]
        target = db.getPlayerEntry(targetID)
        if not target:
            return
        pdata = json.loads(target[2])
        if pdata["TeamID"] != [0, 0]:
            return
        team["Invites"][str(targetID[1])] = {"ID": targetID}
        td.updateTeamData(team, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for x in team['Members']:
            if int(x) in sockets:
                fields["PlayerID"] = targetID
                fields["Socket"] = sockets[int(x)]["Socket"]
                Messaging.sendMessage(24124, fields, sockets[int(x)]['CryptoInit'], calling_instance.player)
        tsock = sockets[int(targetID[1])] if int(targetID[1]) in sockets else None
        if tsock:
            fields["TeamID"] = calling_instance.player.TeamID
            fields["InviterID"] = calling_instance.player.ID
            fields["Socket"] = tsock["Socket"]
            Messaging.sendMessage(24589, fields, tsock['CryptoInit'], calling_instance.player)

    def getMessageType(self):
        return 14370

    def getMessageVersion(self):
        return self.messageVersion
