from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
from Heart.Messaging import Messaging
import json


class TeamLeaveMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        teamdb = TeamDatabaseHandler()
        db = DatabaseHandler()
        pid = calling_instance.player.ID
        low = str(pid[1])
        team_id = list(calling_instance.player.TeamID) if calling_instance.player.TeamID else [0, 0]

        def clear_player():
            calling_instance.player.TeamID = [0, 0]
            row = db.getPlayerEntry(pid)
            if not row:
                return
            pdata = json.loads(row[2])
            pdata["TeamID"] = [0, 0]
            db.updatePlayerData(pdata, calling_instance)

        def send_left():
            fields["Socket"] = calling_instance.client
            Messaging.sendMessage(24125, fields, cryptoInit, calling_instance.player)

        if team_id == [0, 0]:
            clear_player()
            send_left()
            return

        row = teamdb.getTeamWithLowID(team_id[1])
        if not row:
            clear_player()
            send_left()
            return

        team = json.loads(row[0][1])
        if "Members" not in team:
            team["Members"] = {}
        if "Invites" not in team:
            team["Invites"] = {}

        if low in team["Invites"]:
            del team["Invites"][low]

        if low not in team["Members"]:
            teamdb.updateTeamData(team, team_id[1])
            clear_player()
            send_left()
            return

        owner = team["Members"][low]["Owner"]
        sockets = ClientsManager.GetAll()
        del team["Members"][low]

        if len(team["Members"]) == 0:
            teamdb.deleteTeam(team_id[1])
            clear_player()
            send_left()
            return

        if owner:
            first = next(iter(team["Members"]))
            team["Members"][first]["Owner"] = True

        teamdb.updateTeamData(team, team_id[1])
        clear_player()

        for x in team["Members"]:
            if int(x) in sockets:
                out = {"Socket": sockets[int(x)]["Socket"]}
                holder = calling_instance.player
                old = list(holder.TeamID)
                holder.TeamID = team_id
                Messaging.sendMessage(24124, out, sockets[int(x)]["CryptoInit"], holder)
                holder.TeamID = old

        send_left()

    def getMessageType(self):
        return 14353

    def getMessageVersion(self):
        return self.messageVersion
