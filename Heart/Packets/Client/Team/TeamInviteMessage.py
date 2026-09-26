from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
from Heart.Messaging import Messaging
import json


class TeamInviteMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["AccountIDHigh"] = self.readVInt()
        fields["AccountIDLow"] = self.readVInt()
        fields["Side"] = self.readVInt()
        fields["EventSlot"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        team_id = list(calling_instance.player.TeamID) if calling_instance.player.TeamID else [0, 0]
        if team_id == [0, 0]:
            return
        row = td.getTeamWithLowID(team_id[1])
        if not row:
            return
        team = json.loads(row[0][1])
        if "Invites" not in team:
            team["Invites"] = {}
        if "Members" not in team:
            team["Members"] = {}
        targetID = [fields["AccountIDHigh"], fields["AccountIDLow"]]
        tlow = str(targetID[1])
        if tlow in team["Members"]:
            return
        target = db.getPlayerEntry(targetID)
        if not target:
            return
        tdata = json.loads(target[2])
        tid = tdata["TeamID"] if "TeamID" in tdata else [0, 0]
        if tid != [0, 0]:
            return
        iid = list(calling_instance.player.ID)
        team["Invites"][tlow] = {
            "ID": targetID,
            "InviterID": iid,
            "Side": fields["Side"]
        }
        td.updateTeamData(team, team_id[1])
        sockets = ClientsManager.GetAll()
        for low in team["Members"]:
            if int(low) in sockets:
                out = {"Socket": sockets[int(low)]["Socket"]}
                Messaging.sendMessage(24124, out, sockets[int(low)]["CryptoInit"], calling_instance.player)
        if int(targetID[1]) in sockets:
            out = {
                "Socket": sockets[int(targetID[1])]["Socket"],
                "TeamID": team_id,
                "InviterID": iid
            }
            Messaging.sendMessage(24589, out, sockets[int(targetID[1])]["CryptoInit"], calling_instance.player)

    def getMessageType(self):
        return 14365

    def getMessageVersion(self):
        return self.messageVersion
