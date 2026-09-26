from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
from Heart.Messaging import Messaging
import json


class TeamMemberStatusMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["PlayerState"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        print(f"Player {calling_instance.player.ID} changed status to {fields['PlayerState']}")
        team = json.loads(td.getTeamWithLowID(calling_instance.player.TeamID[1])[0][1])
        team["Members"][str(calling_instance.player.ID[1])]["Status"] = fields["PlayerState"]
        team["Members"][str(calling_instance.player.ID[1])]["Ready"] = False
        td.updateTeamData(team, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for low in team["Members"]:
            if int(low) in sockets:
                fields["Socket"] = sockets[int(low)]["Socket"]
                Messaging.sendMessage(24124, fields, sockets[int(low)]["CryptoInit"], calling_instance.player)

    def getMessageType(self):
        return 14361

    def getMessageVersion(self):
        return self.messageVersion
