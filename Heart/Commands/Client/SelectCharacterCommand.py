from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import DatabaseHandler, TeamDatabaseHandler
import json


class SelectCharacterCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        calling_instance.readVInt()
        fields["BrawlerID"] = calling_instance.readVInt()
        fields["Index"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        td = TeamDatabaseHandler()
        row = db.getPlayerEntry(calling_instance.player.ID)
        if row is None:
            return
        pd = json.loads(row[2])
        bid = int(fields["BrawlerID"])
        key = str(bid)
        if key not in pd["OwnedBrawlers"]:
            return
        b = pd["OwnedBrawlers"][key]
        if "StarPower" not in b:
            b["StarPower"] = [23, 0]
        if "Gadget" not in b:
            b["Gadget"] = [23, 0]
        if "Gear1" not in b:
            b["Gear1"] = 0
        if "Gear2" not in b:
            b["Gear2"] = 0
        if "Overcharge" not in b:
            b["Overcharge"] = [0, 0]
        pd["SelectedBrawler"] = bid
        sid = pd["SelectedSkin"]
        pd["SelectedSkin"] = sid if sid in pd["OwnedSkins"] else 0
        pd["SelectedSkins"][key] = pd["SelectedSkin"]
        db.updatePlayerData(pd, calling_instance)
        calling_instance.player.SelectedBrawler = bid
        calling_instance.player.SelectedSkin = pd["SelectedSkin"]
        calling_instance.player.OwnedBrawlers = pd["OwnedBrawlers"]
        calling_instance.player.SelectedSkins = pd["SelectedSkins"]
        team_id = pd["TeamID"]
        if team_id == [0, 0]:
            return
        team_row = td.getTeamWithLowID(team_id[1])
        if team_row is None:
            return
        team = json.loads(team_row[0][1])
        low = str(calling_instance.player.ID[1])
        if low not in team["Members"]:
            return
        member = team["Members"][low]
        member["Brawler"] = [16, bid]
        member["Skin"] = [29, pd["SelectedSkin"]] if pd["SelectedSkin"] > 0 else [0, 0]
        member["StarPower"] = b["StarPower"]
        member["Gadget"] = b["Gadget"]
        member["Gear1"] = b["Gear1"]
        member["Gear2"] = b["Gear2"]
        member["Overcharge"] = b["Overcharge"]
        td.updateTeamData(team, team_id[1])
        sockets = ClientsManager.GetAll()
        for x in team["Members"]:
            if int(x) in sockets:
                Messaging.sendMessage(24124, {"Socket": sockets[int(x)]["Socket"]}, sockets[int(x)]["CryptoInit"], calling_instance.player)

    def getCommandType(self):
        return 525
