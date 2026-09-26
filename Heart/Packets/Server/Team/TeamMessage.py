from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import TeamDatabaseHandler, DatabaseHandler
import json


class TeamMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        td = TeamDatabaseHandler()
        db = DatabaseHandler()
        if not player.TeamID or player.TeamID == [0, 0]:
            return
        row = td.getTeamWithLowID(player.TeamID[1])
        if not row:
            return
        team = json.loads(row[0][1])
        if "Members" not in team:
            team["Members"] = {}
        if "Invites" not in team:
            team["Invites"] = {}
        self.writeVInt(team["Type"] if "Type" in team else 1)
        self.writeBoolean(False)
        self.writeVInt(3)
        self.writeLong(team["HighID"], team["LowID"])
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeDataReference(15, team["mapID"] if "mapID" in team else 0)
        self.writeBoolean(False)
        self.writeVInt(len(team["Members"]))
        for x in team["Members"]:
            member = team["Members"][x]
            pdata = json.loads(db.getPlayerEntry([member["HighID"], member["LowID"]])[2])
            bid = pdata["SelectedBrawler"]
            skins = pdata["SelectedSkins"] if "SelectedSkins" in pdata else {}
            sid = skins[str(bid)] if str(bid) in skins else 0
            if not sid:
                sid = 0
            b = pdata["OwnedBrawlers"][str(bid)]
            self.writeBoolean(member["Owner"])
            self.writeLong(pdata["ID"][0], pdata["ID"][1])
            self.writeDataReference(16, bid)
            if sid:
                self.writeDataReference(29, sid)
            else:
                self.writeVInt(0)
            self.writeVInt(1000)
            self.writeVInt(b["Trophies"])
            self.writeVInt(b["HighestTrophies"])
            self.writeVInt(b["PowerLevel"])
            self.writeVInt(member["Status"] if "Status" in member else 3)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeString(pdata["Name"])
            self.writeVInt(0)
            self.writeVInt(28000000 + pdata["Thumbnail"])
            self.writeVInt(43000000 + pdata["Namecolor"])
            self.writeVInt(-1)
            sp = b["StarPower"][1] if "StarPower" in b and b["StarPower"] else 0
            gd = b["Gadget"][1] if "Gadget" in b and b["Gadget"] else 0
            g1 = b["Gear1"] if "Gear1" in b else 0
            g2 = b["Gear2"] if "Gear2" in b else 0
            oc = b["Overcharge"][1] if "Overcharge" in b and b["Overcharge"] else 0
            if isinstance(g1, list):
                g1 = g1[1] if len(g1) > 1 else 0
            if isinstance(g2, list):
                g2 = g2[1] if len(g2) > 1 else 0
            sp = sp or 0
            gd = gd or 0
            g1 = g1 or 0
            g2 = g2 or 0
            oc = oc or 0
            print(g1)
            print(g2)
            if sp:
                self.writeDataReference(23, sp)
            else:
                self.writeVInt(0)
            if gd:
                self.writeDataReference(23, gd)
            else:
                self.writeVInt(0)
            if g1:
                self.writeDataReference(62, g1)
            else:
                self.writeVInt(0)
            if g2:
                self.writeDataReference(62, g2)
            else:
                self.writeVInt(0)
            if oc:
                self.writeDataReference(23, oc)
            else:
                self.writeVInt(0)
            self.writeVInt(0)
        iid = None
        for member in team["Members"].values():
            if member["Owner"]:
                iid = [member["HighID"], member["LowID"]]
                break
        if iid is None:
            iid = [team["HighID"], team["LowID"]]
        self.writeVInt(len(team["Invites"]))
        for low in team["Invites"]:
            inv = team["Invites"][low]
            iid = inv["InviterID"] if "InviterID" in inv else iid
            ip = json.loads(db.getPlayerEntry(inv["ID"])[2])
            self.writeLong(iid[0], iid[1])
            self.writeLong(inv["ID"][0], inv["ID"][1])
            self.writeString(ip["Name"])
            self.writeVInt(1)
            self.writeVInt(inv["Side"] if "Side" in inv else 0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(True)
        self.writeBoolean(True)
        self.writeBoolean(True)
        self.writeVInt(0)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24124

    def getMessageVersion(self):
        return self.messageVersion
