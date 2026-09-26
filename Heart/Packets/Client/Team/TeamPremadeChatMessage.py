from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from DB.DatabaseHandler import TeamDatabaseHandler
import json


class TeamPremadeChatMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Unk1"] = self.readVInt()
        fields["MessageDataID"] = self.readVInt()
        fields["Unk2"] = self.readVInt()
        fields["Unk3"] = self.readVInt()
        fields["PremadeID"] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        if calling_instance.player.TeamID == [0, 0]:
            return
        td = TeamDatabaseHandler()
        row = td.getTeamWithLowID(calling_instance.player.TeamID[1])
        if not row:
            return
        team = json.loads(row[0][1])
        low = str(calling_instance.player.ID[1])
        member = team["Members"][low] if low in team["Members"] else None
        if member is None:
            return
        sid = 1
        for entry in team["ChatData"] if "ChatData" in team else []:
            value = entry["StreamID"] if "StreamID" in entry else [0, 0]
            if len(value) > 1 and value[1] >= sid:
                sid = value[1] + 1
        if "ChatData" not in team:
            team["ChatData"] = []
        team["ChatData"].append({
            "StreamType": 8,
            "StreamID": [0, sid],
            "PlayerID": calling_instance.player.ID,
            "PlayerName": calling_instance.player.Name,
            "PlayerRole": 1 if "Owner" in member and member["Owner"] else 0,
            "MessageDataID": fields["MessageDataID"],
            "PremadeID": fields["PremadeID"]
        })
        td.updateTeamData(team, calling_instance.player.TeamID[1])
        sockets = ClientsManager.GetAll()
        for x in team["Members"]:
            socket_id = int(x)
            if socket_id in sockets:
                fields["Socket"] = sockets[socket_id]["Socket"]
                Messaging.sendMessage(24131, fields, sockets[socket_id]["CryptoInit"], calling_instance.player)

    def getMessageType(self):
        return 14369

    def getMessageVersion(self):
        return self.messageVersion
