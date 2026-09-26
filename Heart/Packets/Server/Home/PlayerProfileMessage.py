
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import datetime
import time
import random
import json


class PlayerProfileMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        db_instance = DatabaseHandler()
        cdb = ClubDatabaseHandler()

        id = [fields["PlayerHighID"], fields["PlayerLowID"]]
        player_data = json.loads(db_instance.getPlayerEntry(id)[2])

        print(player_data)

        self.writeVLong(fields["PlayerHighID"], fields["PlayerLowID"])
        self.writeDataReference(16, player_data["FavouriteBrawler"])

        print(player_data["FavouriteBrawler"])

        sortedBrawlers = sorted(player_data["OwnedBrawlers"], key=lambda x: player_data["OwnedBrawlers"][x]["Trophies"], reverse=True)

        self.writeVInt(len(sortedBrawlers))

        for brawlerID in sortedBrawlers:
            brawlerData = player_data["OwnedBrawlers"][brawlerID]

            self.writeDataReference(16, brawlerID)
            self.writeDataReference(0)
            self.writeVInt(brawlerData["Trophies"])
            self.writeVInt(brawlerData["HighestTrophies"])
            self.writeVInt(brawlerData["PowerLevel"])

        self.writeVInt(18)

        self.writeVInt(1)
        self.writeVInt(0)

        self.writeVInt(2)
        self.writeVInt(528859)

        self.writeVInt(3)
        self.writeVInt(player_data["Trophies"])

        self.writeVInt(4)
        self.writeVInt(player_data["Trophies"])

        self.writeVInt(5)
        self.writeVInt(len(sortedBrawlers))

        self.writeVInt(8)
        self.writeVInt(0)

        self.writeVInt(11)
        self.writeVInt(0)

        self.writeVInt(9)
        self.writeVInt(0)

        self.writeVInt(12)
        self.writeVInt(0)

        self.writeVInt(13)
        self.writeVInt(0)

        self.writeVInt(14)
        self.writeVInt(0)

        self.writeVInt(15)
        self.writeVInt(0)

        self.writeVInt(16)
        self.writeVInt(0)

        self.writeVInt(18)
        self.writeVInt(19)

        self.writeVInt(17)
        self.writeVInt(19)

        self.writeVInt(19)
        self.writeVInt(0)

        self.writeVInt(20)
        self.writeVInt(0)

        self.writeVInt(21)
        self.writeVInt(502052)

        self.writeString(player_data["Name"])
        self.writeVInt(100)
        self.writeVInt(28000000 + player_data["Thumbnail"])
        self.writeVInt(43000000 + player_data["Namecolor"])

        try:
            player_data["BrawlPassActive"]
        except KeyError:
            player_data["BrawlPassActive"] = False

        if player_data["BrawlPassActive"]:
            self.writeVInt(46000000 + player_data["Namecolor"])
        else:
            self.writeVInt(-1)

        self.writeBoolean(True)
        self.writeVInt(300)

        self.writeString("hello world")
        self.writeVInt(100)
        self.writeVInt(200)

        try:
            self.writeDataReference(29, player_data["SelectedSkins"][f'{player_data["FavouriteBrawler"]}'])
            print("selskins", player_data["SelectedSkins"][f'{player_data["FavouriteBrawler"]}'])
        except:
            self.writeDataReference(0)

        if player.BattleIcon1 == 0:
            self.writeDataReference(0)
        else:
            self.writeDataReference(28, player_data["BattleIcon1"])

        if player.BattleIcon2 == 0:
            self.writeDataReference(0)
        else:
            self.writeDataReference(28, player_data["BattleIcon2"])

        if player.BattleEmote == 0:
            self.writeDataReference(0)
        else:
            self.writeDataReference(52, player_data["BattleEmote"])

        if player.Title == 0:
            self.writeDataReference(0)
        else:
            self.writeDataReference(76, player_data["Title"])

        club = cdb.getClubWithLowID(player_data["AllianceID"][1])

        self.writeBoolean(bool(club))

        if club:
            club_data = json.loads(club[0][1])

            self.writeLong(club_data["HighID"], club_data["LowID"])
            self.writeString(club_data["Name"])
            self.writeDataReference(8, club_data["BadgeID"])
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeDataReference(0)
            self.writeString()
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)

        self.writeDataReference(0)
        self.writeVInt(0)

    def decode(self):
        pass
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24113

    def getMessageVersion(self):
        return self.messageVersion