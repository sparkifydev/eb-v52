
from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
from Heart.Readers.CSVReaders.Cards import Cards
import json

class LogicPurchaseBrawlerCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        fields["Tick1"] = calling_instance.readVInt()
        fields["Unk1"] = calling_instance.readVInt()
        fields["Unk2"] = calling_instance.readVInt()
        fields["VInst1"] = calling_instance.readVInt()
        fields["BrawlerID"] = calling_instance.readDataReference()
        fields["Unk3"] = calling_instance.readVInt()
        fields["Unk"] = calling_instance.readVInt()
        print(fields["Unk"])
        print(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        fields["IsBrawlPassReward"] = False
        box = {'Type': 100, 'Items': []}

        def giveDeliveryBrawler(brawler, bcard, powerlevel):
            playerData["OwnedBrawlers"][brawler] = {
                'CardID': bcard,
                'Skins': [0],
                'Trophies': 0,
                'HighestTrophies': 0,
                'PowerLevel': powerlevel,
                'PowerPoints': 0,
                'State': 2,
                'MasteryPoints': 0,
                'MasteryTier': 0
            }
            playerData["GatchaItems"] = {'Boxes': []}
            item = {'Amount': 1, 'DataRef': [16, brawler], 'RewardID': 1}
            box['Items'].append(item)
            playerData["GatchaItems"]['Boxes'].append(box)

        def changeResourceNegative(resource, amount):
            playerData[resource] -= amount

        def sendDelivery():
            db_instance.updatePlayerData(playerData, calling_instance)
            fields["StarrDrops"] = False
            fields["Socket"] = calling_instance.client
            fields["Command"] = {"ID": 203}
            fields["PlayerID"] = calling_instance.player.ID
            Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
            fields["Socket"] = calling_instance.client
            fields["Command"] = {"ID": 227}
            fields["PlayerID"] = calling_instance.player.ID
            Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)

        def clearBox():
            box['Items'].clear()

        bcard = 0
        gcost = 0
        rare = [1, 2, 3, 6, 8, 10, 13, 24]
        super_rare = [4, 7, 9, 18, 19, 22, 25, 27, 34, 61]
        epic = [14, 15, 16, 20, 26, 29, 30, 36, 43, 45, 48, 50, 58, 69]
        mythic = [11, 17, 21, 31, 32, 37, 42, 47, 64, 67, 71]
        legendary = [5, 12, 23, 28, 40, 52, 63]
        chromatic = [35, 38, 39, 41, 44, 46, 49, 51, 53, 54, 56, 57, 59, 60, 62, 65, 66, 68, 70, 72]

        if fields["BrawlerID"][1] == 1: bcard = 4
        elif fields["BrawlerID"][1] == 2: bcard = 8
        elif fields["BrawlerID"][1] == 3: bcard = 12
        elif fields["BrawlerID"][1] == 4: bcard = 16
        elif fields["BrawlerID"][1] == 5: bcard = 20
        elif fields["BrawlerID"][1] == 6: bcard = 24
        elif fields["BrawlerID"][1] == 7: bcard = 28
        elif fields["BrawlerID"][1] == 8: bcard = 32
        elif fields["BrawlerID"][1] == 9: bcard = 36
        elif fields["BrawlerID"][1] == 10: bcard = 40
        elif fields["BrawlerID"][1] == 11: bcard = 44
        elif fields["BrawlerID"][1] == 12: bcard = 48
        elif fields["BrawlerID"][1] == 13: bcard = 52
        elif fields["BrawlerID"][1] == 14: bcard = 56
        elif fields["BrawlerID"][1] == 15: bcard = 60
        elif fields["BrawlerID"][1] == 16: bcard = 64
        elif fields["BrawlerID"][1] == 17: bcard = 68
        elif fields["BrawlerID"][1] == 18: bcard = 72
        elif fields["BrawlerID"][1] == 19: bcard = 95
        elif fields["BrawlerID"][1] == 20: bcard = 100
        elif fields["BrawlerID"][1] == 21: bcard = 105
        elif fields["BrawlerID"][1] == 22: bcard = 110
        elif fields["BrawlerID"][1] == 23: bcard = 115
        elif fields["BrawlerID"][1] == 24: bcard = 120
        elif fields["BrawlerID"][1] == 25: bcard = 125
        elif fields["BrawlerID"][1] == 26: bcard = 130
        elif fields["BrawlerID"][1] == 27: bcard = 177
        elif fields["BrawlerID"][1] == 28: bcard = 182
        elif fields["BrawlerID"][1] == 29: bcard = 188
        elif fields["BrawlerID"][1] == 30: bcard = 194
        elif fields["BrawlerID"][1] == 31: bcard = 200
        elif fields["BrawlerID"][1] == 32: bcard = 206
        elif fields["BrawlerID"][1] == 34: bcard = 218
        elif fields["BrawlerID"][1] == 35: bcard = 224
        elif fields["BrawlerID"][1] == 36: bcard = 230
        elif fields["BrawlerID"][1] == 37: bcard = 236
        elif fields["BrawlerID"][1] == 38: bcard = 279
        elif fields["BrawlerID"][1] == 39: bcard = 296
        elif fields["BrawlerID"][1] == 40: bcard = 303
        elif fields["BrawlerID"][1] == 41: bcard = 320
        elif fields["BrawlerID"][1] == 42: bcard = 327
        elif fields["BrawlerID"][1] == 43: bcard = 334
        elif fields["BrawlerID"][1] == 44: bcard = 341
        elif fields["BrawlerID"][1] == 45: bcard = 358
        elif fields["BrawlerID"][1] == 46: bcard = 365
        elif fields["BrawlerID"][1] == 47: bcard = 372
        elif fields["BrawlerID"][1] == 48: bcard = 379
        elif fields["BrawlerID"][1] == 49: bcard = 386
        elif fields["BrawlerID"][1] == 50: bcard = 393
        elif fields["BrawlerID"][1] == 51: bcard = 410
        elif fields["BrawlerID"][1] == 52: bcard = 417
        elif fields["BrawlerID"][1] == 53: bcard = 427
        elif fields["BrawlerID"][1] == 54: bcard = 434
        elif fields["BrawlerID"][1] == 56: bcard = 448
        elif fields["BrawlerID"][1] == 57: bcard = 466
        elif fields["BrawlerID"][1] == 58: bcard = 474
        elif fields["BrawlerID"][1] == 59: bcard = 491
        elif fields["BrawlerID"][1] == 60: bcard = 499
        elif fields["BrawlerID"][1] == 61: bcard = 605
        elif fields["BrawlerID"][1] == 62: bcard = 515
        elif fields["BrawlerID"][1] == 63: bcard = 523
        elif fields["BrawlerID"][1] == 64: bcard = 531
        elif fields["BrawlerID"][1] == 65: bcard = 539
        elif fields["BrawlerID"][1] == 66: bcard = 547
        elif fields["BrawlerID"][1] == 67: bcard = 557
        elif fields["BrawlerID"][1] == 68: bcard = 565
        elif fields["BrawlerID"][1] == 69: bcard = 573
        elif fields["BrawlerID"][1] == 70: bcard = 581
        elif fields["BrawlerID"][1] == 71: bcard = 589
        elif fields["BrawlerID"][1] == 72: bcard = 597
        elif fields["BrawlerID"][1] == 73: bcard = 605

        if fields["BrawlerID"][1] in rare: gcost = 29
        elif fields["BrawlerID"][1] in super_rare: gcost = 79
        elif fields["BrawlerID"][1] in epic: gcost = 169
        elif fields["BrawlerID"][1] in mythic: gcost = 349
        elif fields["BrawlerID"][1] in legendary: gcost = 699
        elif fields["BrawlerID"][1] in chromatic: gcost = 0

        if fields["Unk"] in (0, 20):
            if fields["BrawlerID"][1] in chromatic:
                giveDeliveryBrawler(fields["BrawlerID"][1], bcard, 1)
                if fields["BrawlerID"][1] == 72 and playerData["ChromaticCoins"] >= 1250:
                    changeResourceNegative("ChromaticCoins", 1250)
                elif playerData["ChromaticCoins"] >= 500:
                    changeResourceNegative("ChromaticCoins", 500)
                else:
                    changeResourceNegative("Gems", 349)
                if fields["BrawlerID"][1] in playerData["Brawlers"]:
                    playerData["Brawlers"].remove(fields["BrawlerID"][1])
                sendDelivery()
                clearBox()
            else:
                if fields["BrawlerID"][1] in playerData["Brawlers"] or fields["BrawlerID"][1] == playerData["RecruitBrawler"]:
                    giveDeliveryBrawler(fields["BrawlerID"][1], bcard, 1)
                    if fields["BrawlerID"][1] in playerData["Brawlers"]:
                        playerData["Brawlers"].remove(fields["BrawlerID"][1])
                    if fields["BrawlerID"][1] == playerData["RecruitBrawler"]:
                        playerData["RecruitBrawler"] += 1
                    changeResourceNegative("Gems", gcost)
                    sendDelivery()
                    clearBox()

    def getCommandType(self):
        return 560
