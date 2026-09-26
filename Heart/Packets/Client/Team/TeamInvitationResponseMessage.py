from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Messaging import Messaging
from DB.DatabaseHandler import TeamDatabaseHandler, DatabaseHandler
import json


class TeamInvitationResponseMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        pass

    def decode(self):
        fields = {}
        fields['Response'] = self.readVInt()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        target = None
        for raw in td.getAllTeam():
            if str(calling_instance.player.ID[1]) in raw['Invites']:
                target = raw
                break
        if target is None or fields['Response'] != 1:
            return
        team = json.loads(td.getTeamWithLowID(target['LowID'])[0][1])
        pdata = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        if str(calling_instance.player.ID[1]) not in team['Invites']:
            return
        if len(team['Members']) >= 3:
            return
        del team['Invites'][str(calling_instance.player.ID[1])]
        team['Members'][str(calling_instance.player.ID[1])] = {
            'HighID': calling_instance.player.ID[0],
            'LowID': calling_instance.player.ID[1],
            'Ready': False,
            'Status': 0,
            'Owner': False,
            'TeamIndex': len(team['Members'])
        }
        pdata['TeamID'] = [team['HighID'], team['LowID']]
        db.updatePlayerData(pdata, calling_instance)
        td.updateTeamData(team, team['LowID'])
        sockets = ClientsManager.GetAll()
        for x in team['Members']:
            if int(x) in sockets:
                out = {'Socket': sockets[int(x)]['Socket']}
                Messaging.sendMessage(24124, out, sockets[int(x)]['CryptoInit'], calling_instance.player)
                Messaging.sendMessage(24131, out, sockets[int(x)]['CryptoInit'], calling_instance.player)

    def getMessageType(self):
        return 14368

    def getMessageVersion(self):
        return self.messageVersion
