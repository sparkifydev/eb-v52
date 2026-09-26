import json
from Heart.Commands.LogicCommand import LogicCommand
from DB.DatabaseHandler import DatabaseHandler
from Heart.Readers.CSVReaders.Cards import Cards
from Heart.Messaging import Messaging

class LogicStarRoadRewardCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        fields["UnlockedBrawler"] = calling_instance.readVInt()
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        if fields["UnlockedBrawler"] == 1:
            playerData["RecruitBrawlerCard"] = 4
            playerData["RecruitBrawler"] = 2
            if 2 in playerData["Brawlers"]: playerData["Brawlers"].remove(2)
        if fields["UnlockedBrawler"] == 2:
            playerData["RecruitBrawlerCard"] = 8
            playerData["RecruitBrawler"] = 3
            if 3 in playerData["Brawlers"]: playerData["Brawlers"].remove(3)
        if fields["UnlockedBrawler"] == 3:
            playerData["RecruitBrawlerCard"] = 12
            playerData["RecruitBrawler"] = 4
            if 4 in playerData["Brawlers"]: playerData["Brawlers"].remove(4)
        if fields["UnlockedBrawler"] == 4:
            playerData["RecruitBrawlerCard"] = 16
            playerData["RecruitBrawler"] = 5
            if 5 in playerData["Brawlers"]: playerData["Brawlers"].remove(5)
        if fields["UnlockedBrawler"] == 5:
            playerData["RecruitBrawlerCard"] = 20
            playerData["RecruitBrawler"] = 6
            if 6 in playerData["Brawlers"]: playerData["Brawlers"].remove(6)
        if fields["UnlockedBrawler"] == 6:
            playerData["RecruitBrawlerCard"] = 24
            playerData["RecruitBrawler"] = 7
            if 7 in playerData["Brawlers"]: playerData["Brawlers"].remove(7)
        if fields["UnlockedBrawler"] == 7:
            playerData["RecruitBrawlerCard"] = 28
            playerData["RecruitBrawler"] = 8
            if 8 in playerData["Brawlers"]: playerData["Brawlers"].remove(8)
        if fields["UnlockedBrawler"] == 8:
            playerData["RecruitBrawlerCard"] = 32
            playerData["RecruitBrawler"] = 9
            if 9 in playerData["Brawlers"]: playerData["Brawlers"].remove(9)
        if fields["UnlockedBrawler"] == 9:
            playerData["RecruitBrawlerCard"] = 36
            playerData["RecruitBrawler"] = 10
            if 10 in playerData["Brawlers"]: playerData["Brawlers"].remove(10)
        if fields["UnlockedBrawler"] == 10:
            playerData["RecruitBrawlerCard"] = 40
            playerData["RecruitBrawler"] = 11
            if 11 in playerData["Brawlers"]: playerData["Brawlers"].remove(11)
        if fields["UnlockedBrawler"] == 11:
            playerData["RecruitBrawlerCard"] = 44
            playerData["RecruitBrawler"] = 12
            if 12 in playerData["Brawlers"]: playerData["Brawlers"].remove(12)
        if fields["UnlockedBrawler"] == 12:
            playerData["RecruitBrawlerCard"] = 48
            playerData["RecruitBrawler"] = 13
            if 13 in playerData["Brawlers"]: playerData["Brawlers"].remove(13)
        if fields["UnlockedBrawler"] == 13:
            playerData["RecruitBrawlerCard"] = 52
            playerData["RecruitBrawler"] = 14
            if 14 in playerData["Brawlers"]: playerData["Brawlers"].remove(14)
        if fields["UnlockedBrawler"] == 14:
            playerData["RecruitBrawlerCard"] = 56
            playerData["RecruitBrawler"] = 15
            if 15 in playerData["Brawlers"]: playerData["Brawlers"].remove(15)
        if fields["UnlockedBrawler"] == 15:
            playerData["RecruitBrawlerCard"] = 60
            playerData["RecruitBrawler"] = 16
            if 16 in playerData["Brawlers"]: playerData["Brawlers"].remove(16)
        if fields["UnlockedBrawler"] == 16:
            playerData["RecruitBrawlerCard"] = 64
            playerData["RecruitBrawler"] = 17
            if 17 in playerData["Brawlers"]: playerData["Brawlers"].remove(17)
        if fields["UnlockedBrawler"] == 17:
            playerData["RecruitBrawlerCard"] = 68
            playerData["RecruitBrawler"] = 18
            if 18 in playerData["Brawlers"]: playerData["Brawlers"].remove(18)
        if fields["UnlockedBrawler"] == 18:
            playerData["RecruitBrawlerCard"] = 72
            playerData["RecruitBrawler"] = 19
            if 19 in playerData["Brawlers"]: playerData["Brawlers"].remove(19)
        if fields["UnlockedBrawler"] == 19:
            playerData["RecruitBrawlerCard"] = 95
            playerData["RecruitBrawler"] = 20
            if 20 in playerData["Brawlers"]: playerData["Brawlers"].remove(20)
        if fields["UnlockedBrawler"] == 20:
            playerData["RecruitBrawlerCard"] = 100
            playerData["RecruitBrawler"] = 21
            if 21 in playerData["Brawlers"]: playerData["Brawlers"].remove(21)
        if fields["UnlockedBrawler"] == 21:
            playerData["RecruitBrawlerCard"] = 105
            playerData["RecruitBrawler"] = 22
            if 22 in playerData["Brawlers"]: playerData["Brawlers"].remove(22)
        if fields["UnlockedBrawler"] == 22:
            playerData["RecruitBrawlerCard"] = 110
            playerData["RecruitBrawler"] = 23
            if 23 in playerData["Brawlers"]: playerData["Brawlers"].remove(23)
        if fields["UnlockedBrawler"] == 23:
            playerData["RecruitBrawlerCard"] = 115
            playerData["RecruitBrawler"] = 24
            if 24 in playerData["Brawlers"]: playerData["Brawlers"].remove(24)
        if fields["UnlockedBrawler"] == 24:
            playerData["RecruitBrawlerCard"] = 120
            playerData["RecruitBrawler"] = 25
            if 25 in playerData["Brawlers"]: playerData["Brawlers"].remove(25)
        if fields["UnlockedBrawler"] == 25:
            playerData["RecruitBrawlerCard"] = 125
            playerData["RecruitBrawler"] = 26
            if 26 in playerData["Brawlers"]: playerData["Brawlers"].remove(26)
        if fields["UnlockedBrawler"] == 26:
            playerData["RecruitBrawlerCard"] = 130
            playerData["RecruitBrawler"] = 27
            if 27 in playerData["Brawlers"]: playerData["Brawlers"].remove(27)
        if fields["UnlockedBrawler"] == 27:
            playerData["RecruitBrawlerCard"] = 177
            playerData["RecruitBrawler"] = 28
            if 28 in playerData["Brawlers"]: playerData["Brawlers"].remove(28)
        if fields["UnlockedBrawler"] == 28:
            playerData["RecruitBrawlerCard"] = 182
            playerData["RecruitBrawler"] = 29
            if 29 in playerData["Brawlers"]: playerData["Brawlers"].remove(29)
        if fields["UnlockedBrawler"] == 29:
            playerData["RecruitBrawlerCard"] = 188
            playerData["RecruitBrawler"] = 30
            if 30 in playerData["Brawlers"]: playerData["Brawlers"].remove(30)
        if fields["UnlockedBrawler"] == 30:
            playerData["RecruitBrawlerCard"] = 194
            playerData["RecruitBrawler"] = 31
            if 31 in playerData["Brawlers"]: playerData["Brawlers"].remove(31)
        if fields["UnlockedBrawler"] == 31:
            playerData["RecruitBrawlerCard"] = 200
            playerData["RecruitBrawler"] = 32
            if 32 in playerData["Brawlers"]: playerData["Brawlers"].remove(32)
        if fields["UnlockedBrawler"] == 32:
            playerData["RecruitBrawlerCard"] = 206
            playerData["RecruitBrawler"] = 34
            if 34 in playerData["Brawlers"]: playerData["Brawlers"].remove(34)
        if fields["UnlockedBrawler"] == 34:
            playerData["RecruitBrawlerCard"] = 218
            playerData["RecruitBrawler"] = 36
            if 36 in playerData["Brawlers"]: playerData["Brawlers"].remove(36)
        if fields["UnlockedBrawler"] == 36:
            playerData["RecruitBrawlerCard"] = 230
            playerData["RecruitBrawler"] = 37
            if 37 in playerData["Brawlers"]: playerData["Brawlers"].remove(37)
        if fields["UnlockedBrawler"] == 37:
            playerData["RecruitBrawlerCard"] = 236
            playerData["RecruitBrawler"] = 40
            if 40 in playerData["Brawlers"]: playerData["Brawlers"].remove(40)
        if fields["UnlockedBrawler"] == 40:
            playerData["RecruitBrawlerCard"] = 303
            playerData["RecruitBrawler"] = 42
            if 42 in playerData["Brawlers"]: playerData["Brawlers"].remove(42)
        if fields["UnlockedBrawler"] == 42:
            playerData["RecruitBrawlerCard"] = 327
            playerData["RecruitBrawler"] = 43
            if 43 in playerData["Brawlers"]: playerData["Brawlers"].remove(43)
        if fields["UnlockedBrawler"] == 43:
            playerData["RecruitBrawlerCard"] = 334
            playerData["RecruitBrawler"] = 45
            if 45 in playerData["Brawlers"]: playerData["Brawlers"].remove(45)
        if fields["UnlockedBrawler"] == 45:
            playerData["RecruitBrawlerCard"] = 358
            playerData["RecruitBrawler"] = 47
            if 47 in playerData["Brawlers"]: playerData["Brawlers"].remove(47)
        if fields["UnlockedBrawler"] == 47:
            playerData["RecruitBrawlerCard"] = 372
            playerData["RecruitBrawler"] = 48
            if 48 in playerData["Brawlers"]: playerData["Brawlers"].remove(48)
        if fields["UnlockedBrawler"] == 48:
            playerData["RecruitBrawlerCard"] = 379
            playerData["RecruitBrawler"] = 50
            if 50 in playerData["Brawlers"]: playerData["Brawlers"].remove(50)
        if fields["UnlockedBrawler"] == 50:
            playerData["RecruitBrawlerCard"] = 393
            playerData["RecruitBrawler"] = 52
            if 52 in playerData["Brawlers"]: playerData["Brawlers"].remove(52)
        if fields["UnlockedBrawler"] == 52:
            playerData["RecruitBrawlerCard"] = 417
            playerData["RecruitBrawler"] = 58
            if 58 in playerData["Brawlers"]: playerData["Brawlers"].remove(58)
        if fields["UnlockedBrawler"] == 58:
            playerData["RecruitBrawlerCard"] = 474
            playerData["RecruitBrawler"] = 61
            if 61 in playerData["Brawlers"]: playerData["Brawlers"].remove(61)
        if fields["UnlockedBrawler"] == 61:
            playerData["RecruitBrawlerCard"] = 605
            playerData["RecruitBrawler"] = 63
            if 63 in playerData["Brawlers"]: playerData["Brawlers"].remove(63)
        if fields["UnlockedBrawler"] == 63:
            playerData["RecruitBrawlerCard"] = 523
            playerData["RecruitBrawler"] = 64
            if 64 in playerData["Brawlers"]: playerData["Brawlers"].remove(64)
        if fields["UnlockedBrawler"] == 64:
            playerData["RecruitBrawlerCard"] = 531
            playerData["RecruitBrawler"] = 67
            if 67 in playerData["Brawlers"]: playerData["Brawlers"].remove(67)
        if fields["UnlockedBrawler"] == 67:
            playerData["RecruitBrawlerCard"] = 557
            playerData["RecruitBrawler"] = 69
            if 69 in playerData["Brawlers"]: playerData["Brawlers"].remove(69)
        if fields["UnlockedBrawler"] == 69:
            playerData["RecruitBrawlerCard"] = 573
            playerData["RecruitBrawler"] = 71
            if 71 in playerData["Brawlers"]: playerData["Brawlers"].remove(71)
        if fields["UnlockedBrawler"] == 71:
            playerData["RecruitBrawlerCard"] = 589
            playerData["RecruitBrawler"] = 73
            if 73 in playerData["Brawlers"]: playerData["Brawlers"].remove(73)
        if fields["UnlockedBrawler"] == 73:
            playerData["RecruitBrawlerCard"] = 605
        cardID = playerData["RecruitBrawlerCard"]
            
        rare = [1, 2, 3, 6, 8, 10, 13, 24]
        super_rare = [4, 7, 9, 18, 19, 22, 25, 27, 34, 61]
        epic = [14, 15, 16, 20, 26, 29, 30, 36, 43, 45, 48, 50, 58, 69]
        mythic = [11, 17, 21, 35, 31, 32, 37, 42, 47, 64, 67, 71]
        legendary = [5, 12, 23, 28, 40, 52, 63]
        
        ja = fields["UnlockedBrawler"]
        
        if ja in rare:
            playerData["RecruitTokens"] = playerData["RecruitTokens"] - 160
        if ja in super_rare:
            playerData["RecruitTokens"] = playerData["RecruitTokens"] - 430
        if ja in epic:
            playerData["RecruitTokens"] = playerData["RecruitTokens"] - 925
        if ja in mythic:
            playerData["RecruitTokens"] = playerData["RecruitTokens"] - 1900
        if ja in legendary:
            playerData["RecruitTokens"] = playerData["RecruitTokens"] - 3800
        
        playerData["OwnedBrawlers"][ja] = {'CardID': cardID, 'Skins': [0], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'MasteryPoints': 0, 'MasteryTier': 0}
        
        db_instance.updatePlayerData(playerData, calling_instance)
        fields["Socket"] = calling_instance.client
        fields["Command"] = {"ID": 227}
        fields["PlayerID"] = calling_instance.player.ID
        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)

        db_instance.updatePlayerData(playerData, calling_instance)
        fields['NoAnim'] = True
        fields["Command"] = {"ID": 203}
        fields["PlayerID"] = calling_instance.player.ID
        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player) 

    def getCommandType(self):
        return 562