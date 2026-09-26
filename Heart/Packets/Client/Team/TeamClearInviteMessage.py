from Heart.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from DB.DatabaseHandler import TeamDatabaseHandler, DatabaseHandler
from Heart.Instances.Heart.Team import Team
from Heart.Utility import Utility
import json


class TeamClearInviteMessage(PiranhaMessage):


    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0


    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["PlayerID"] = self.readLong()
        super().decode(fields)
        return fields


    def execute(message, calling_instance, fields):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        pdata = json.loads(db.getPlayerEntry(fields["PlayerID"])[2])
        teamData = json.loads(td.getTeamWithLowID(calling_instance.player.TeamID[1])[0][1])
        
        del teamData["Invites"][str(fields["PlayerID"][1])]
        td.updateTeamData(teamData, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for x in teamData["Members"]:
            if int(x) in sockets:
                fields["Socket"] = sockets[int(x)]["Socket"]
                Messaging.sendMessage(24124, fields, calling_instance.player)


    def getMessageType(self):
        return 14367


    def getMessageVersion(self):
        return self.messageVersion
