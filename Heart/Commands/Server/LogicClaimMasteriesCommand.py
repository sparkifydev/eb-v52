
from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
from Heart.Readers.CSVReaders.Masteries import Masteries
import json


class LogicClaimMasteriesCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        fields["tick1"] = calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        fields["brawler"] = calling_instance.readDataReference()
        fields["reward"] = calling_instance.readVInt()
        print(fields["brawler"])
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])

        rare = [0, 1, 2, 3, 6, 8, 10, 13, 24]
        super_rare = [4, 7, 9, 18, 19, 22, 25, 27, 34, 61]
        epic = [14, 15, 16, 20, 26, 29, 30, 36, 43, 45, 48, 50, 58, 69]
        mythic = [11, 17, 21, 31, 32, 37, 42, 47, 64, 67, 71]
        chromatic = [35, 38, 39, 41, 44, 46, 49, 51, 53, 54, 56, 57, 59, 60, 62, 65, 66, 68, 70, 72]

        bid = fields["brawler"][1]
        mifiki = bid in mythic or bid not in rare + super_rare + epic + mythic

        box = {"Items": []}

        if fields["reward"] == 2:
            amount = 1000 if mifiki else 750
            item = {"Amount": amount, "DataRef": [0, 0], "RewardID": 7}
            player_data["Coins"] += amount

        elif fields["reward"] == 3:
            amount = 150 if mifiki else 100
            item = {"Amount": amount, "DataRef": [16, 0], "RewardID": 24}
            player_data["PowerPoints"] += amount

        elif fields["reward"] == 4:
            amount = 100 if mifiki else 75
            item = {"Amount": amount, "DataRef": [16, 0], "RewardID": 22}
            player_data["RecruitTokens"] += amount

        elif fields["reward"] == 5:
            amount = 300 if mifiki else 200
            item = {"Amount": amount, "DataRef": [16, 0], "RewardID": 24}
            player_data["PowerPoints"] += amount

        elif fields["reward"] == 6:
            amount = 2000 if mifiki else 1250
            item = {"Amount": amount, "DataRef": [0, 0], "RewardID": 7}
            player_data["Coins"] += amount

        elif fields["reward"] == 7:
            if bid in chromatic:
                amount = 100
                item = {"Amount": amount, "DataRef": [16, 0], "RewardID": 23}
                player_data["ChromaticCoins"] += amount
            else:
                amount = 200 if mifiki else 150
                item = {"Amount": amount, "DataRef": [16, 0], "RewardID": 22}
                player_data["RecruitTokens"] += amount

        elif fields["reward"] == 8:
            boxType = 11
            info = Masteries.getMasteryVanityReward(0)
            print(info)
            amount = 1
            data = info.VanityData
            item = {"Amount": amount, "DataRef": [52, data.EmoteID], "RewardID": boxType}
            player_data["OwnedPins"].append(data.EmoteID)

        elif fields["reward"] == 9:
            boxType = 22
            amount = 100
            item = {"Amount": amount, "DataRef": [16, 0], "RewardID": boxType}
            player_data["RecruitTokens"] += amount

        elif fields["reward"] == 10:
            item = {"Amount": 0, "DataRef": [71, 77], "RewardID": 10}

            if "OwnedTitles" not in player_data:
                player_data["OwnedTitles"] = []

            player_data["OwnedTitles"].append(bid)

        else:
            return

        player_data["GatchaItems"] = {"Boxes": []}
        box["Type"] = 100
        box["Items"].append(item)
        player_data["GatchaItems"]["Boxes"].append(box)

        brawler_key = str(bid)

        if brawler_key in player_data["OwnedBrawlers"]:
            player_data["OwnedBrawlers"][brawler_key]["MasteryTier"] += 1

        db_instance.updatePlayerData(player_data, calling_instance)

        fields["IsBrawlPassReward"] = False
        fields["Socket"] = calling_instance.client
        fields["Command"] = {"ID": 203}
        fields["PlayerID"] = calling_instance.player.ID
        fields["ServerChecksum"] = 0
        fields["ClientChecksum"] = 0

        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
