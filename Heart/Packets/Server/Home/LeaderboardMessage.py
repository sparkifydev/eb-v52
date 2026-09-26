from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json


class LeaderboardMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        db = DatabaseHandler()
        cdb = ClubDatabaseHandler()
        ltype = fields["LeaderboardType"]
        hid = fields["HeroDataID"]
        rid = fields["RegionID"]
        regional = fields["IsRegional"]

        self.writeVInt(ltype)
        self.writeVInt(0)
        if hid is None:
            self.writeDataReference(0, 0)
        else:
            self.writeDataReference(hid[0], hid[1])
        if regional:
            self.writeString(player.Region)
        else:
            self.writeString()

        if ltype == 0:
            bid = hid[1]
            players = db.load_all()
            rows = []
            for data in players:
                if "OwnedBrawlers" not in data:
                    continue
                key = str(bid)
                if key not in data["OwnedBrawlers"]:
                    continue
                rows.append(data)
            rows.sort(key=lambda data: data["OwnedBrawlers"][str(bid)]["Trophies"], reverse=True)
            rows = rows[:200]
            self.writeVInt(len(rows))
            for data in rows:
                self.writeVLong(data["ID"][0], data["ID"][1])
                self.writeVInt(1)
                self.writeVInt(data["OwnedBrawlers"][str(bid)]["Trophies"])
                self.writeBoolean(True)
                club = cdb.getClubWithLowID(data["AllianceID"][1])
                print(club)
                name = json.loads(club[0][1])["Name"] if club else None
                if name != None:
                    self.writeString(name)
                else:
                    self.writeString()
                self.writeString(data["Name"])
                self.writeVInt(100)
                self.writeVInt(28000000 + data["Thumbnail"])
                self.writeVInt(43000000)
                self.writeVInt(0)
                self.writeBoolean(False)
            own = 0
            for i in range(len(rows)):
                if rows[i]["ID"] == player.ID:
                    own = i + 1
                    break
            ov = 0
            key = str(bid)
            if "OwnedBrawlers" in player.__dict__ and key in player.OwnedBrawlers:
                ov = player.OwnedBrawlers[key]["Trophies"]
            self.writeVInt(ov)
            self.writeVInt(own)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeString("BS" if regional else "")
            return

        if ltype == 1:
            players = db.getSorted()
            players = players[:200]
            self.writeVInt(len(players))
            rank = 0
            for data in players:
                rank += 1
                self.writeVLong(data["ID"][0], data["ID"][1])
                self.writeVInt(1)
                self.writeVInt(data["Trophies"])
                self.writeBoolean(True)
                club = cdb.getClubWithLowID(data["AllianceID"][1])
                print(club)
                name = json.loads(club[0][1])["Name"] if club else None
                if name != None:
                    self.writeString(name)
                else:
                    self.writeString()
                self.writeString(data["Name"])
                self.writeVInt(100)
                self.writeVInt(28000000 + data["Thumbnail"])
                self.writeVInt(43000000)
                self.writeVInt(0)
                self.writeBoolean(False)
            own = 0
            for i in range(len(players)):
                if players[i]["ID"] == player.ID:
                    own = i + 1
                    break
            self.writeVInt(player.Trophies)
            self.writeVInt(own)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeString("BS" if regional else "")
            return

        if ltype == 2:
            clubs = cdb.getAllClub()
            clubs.sort(key=lambda data: cdb.getTotalTrophies(data), reverse=True)
            clubs = clubs[:200]
            self.writeVInt(len(clubs))
            for i in range(len(clubs)):
                club = clubs[i]
                self.writeVLong(club["HighID"], club["LowID"])
                self.writeVInt(1)
                self.writeVInt(cdb.getTotalTrophies(club))
                self.writeBoolean(False)
                self.writeBoolean(True)
                self.writeString(club["Name"])
                self.writeVInt(len(club["Members"]))
                self.writeDataReference(8, club["BadgeID"])
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeString("BS" if regional else "")
            return

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeString("BS" if regional else "")

    def decode(self):
        return {}

    def execute(self, message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24403

    def getMessageVersion(self):
        return self.messageVersion
