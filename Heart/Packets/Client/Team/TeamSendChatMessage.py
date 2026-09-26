from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import TeamDatabaseHandler
from Heart.Messaging import Messaging
import json


class TeamSendChatMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields["Message"] = self.readString()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        player = calling_instance.player
        if player.TeamID == [0, 0]:
            return

        td = TeamDatabaseHandler()
        row = td.getTeamWithLowID(player.TeamID[1])
        if not row:
            return

        team = json.loads(row[0][1])
        low = str(player.ID[1])
        member = team["Members"].get(low)
        if member is None:
            return

        chat_data = team.setdefault("ChatData", [])
        stream_id = 1
        for entry in chat_data:
            entry_id = entry.get("StreamID", [0, 0])
            if len(entry_id) > 1 and entry_id[1] >= stream_id:
                stream_id = entry_id[1] + 1

        chat_data.append({
            "StreamType": 2,
            "StreamID": [0, stream_id],
            "PlayerID": player.ID,
            "PlayerName": player.Name,
            "PlayerRole": 1 if member.get("Owner") else 0,
            "Message": fields["Message"],
        })
        td.updateTeamData(team, player.TeamID[1])

        sockets = ClientsManager.GetAll()
        for member_low in team["Members"]:
            socket_id = int(member_low)
            if socket_id not in sockets:
                continue
            fields["Socket"] = sockets[socket_id]["Socket"]
            Messaging.sendMessage(
                24131,
                fields,
                sockets[socket_id]["CryptoInit"],
                player,
            )

    def getMessageType(self):
        return 14049

    def getMessageVersion(self):
        return self.messageVersion