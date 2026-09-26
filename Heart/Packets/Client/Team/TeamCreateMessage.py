from Heart.ByteStream import ByteStream
from Heart.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage

from Heart.Messaging import Messaging
from DB.DatabaseHandler import TeamDatabaseHandler, DatabaseHandler
from Heart.Instances.Heart.Team import Team
from Heart.Utility import Utility
import json


class TeamCreateMessage(PiranhaMessage):


    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0


    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Unk"] = self.readVInt()
        fields["mapSlot"] = self.readVInt()
        fields["roomType"] = self.readVInt()
        super().decode(fields)
        return fields


    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()


        fields["mapID"] = 7
        fields["TeamID"] = Utility.getRandomID()
        fields["TeamInfo"] = Team.createTeamData(calling_instance, fields)
        td.createTeam(fields["TeamID"][1], fields["TeamInfo"])
        pdata = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        pdata["TeamID"] = fields["TeamID"]
        db.updatePlayerData(pdata, calling_instance)
        fields["Socket"] = calling_instance.client
        Messaging.sendMessage(24124, fields, cryptoInit, calling_instance.player)
        Messaging.sendMessage(24131, fields, cryptoInit, calling_instance.player)


    def getMessageType(self):
        return 12451


    def getMessageVersion(self):
        return self.messageVersion
