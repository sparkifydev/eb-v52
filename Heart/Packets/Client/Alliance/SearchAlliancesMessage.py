from Heart.Instances.Heart.Alliance import Alliance
from Heart.Messaging import Messaging

from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class SearchAlliancesMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields):
        pass

    def decode(self):
        fields = {}
        fields["SearchString"] = self.readString()
        fields["Unk"] = self.readInt()
        fields["MinMembers"] = self.readInt()
        fields["MaxMembers"] = self.readInt()
        fields["MinTrophies"] = self.readInt()
        fields["FindOnlyJoinableClubs"] = self.readBoolean()
        fields["Score"] = self.readInt()
        fields["MinLevel"] = self.readInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        fields["Socket"] = calling_instance.client
        Messaging.sendMessage(24310, fields, calling_instance.player)

    def getMessageType(self):
        return 14324

    def getMessageVersion(self):
        return self.messageVersion