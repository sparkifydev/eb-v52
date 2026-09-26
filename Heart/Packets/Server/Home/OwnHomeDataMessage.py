from Heart.Record.ByteStreamHelper import ByteStreamHelper
from Heart.Packets.PiranhaMessage import PiranhaMessage
from Heart.Logic.LogicStarrDropData import starrDropOpening

from JSON.JSONHandler import JSONHandler

class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):

        ownedPinsCount = len(player.OwnedPins)
        ownedThumbnailCount = len(player.OwnedThumbnails)
        ownedSprays = len(player.OwnedSprays)

        self.writeVInt(1688816070)
        self.writeVInt(1191532375)
        self.writeVInt(2023189)
        self.writeVInt(73530)

        self.writeVInt(player.Trophies)
        self.writeVInt(player.HighestTrophies)
        self.writeVInt(player.HighestTrophies) 
        self.writeVInt(player.TrophyRoadTier)
        self.writeVInt(player.Experience)
        self.writeDataReference(28, player.Thumbnail)
        self.writeDataReference(43, player.Namecolor)

        self.writeVInt(26)
        for x in range(26):
            self.writeVInt(x)

        if player.SelectedSkin != 0:
        	self.writeVInt(1)
        	self.writeDataReference(29, player.SelectedSkin)
        else:
        	self.writeVInt(0)

        self.writeVInt(0)

        self.writeVInt(0)
        
        self.writeVInt(len(player.OwnedSkins))
        for skinID in player.OwnedSkins:
            self.writeDataReference(29, skinID)

        self.writeVInt(0)

        self.writeVInt(0)

        self.writeVInt(0)
        self.writeVInt(player.HighestTrophies)
        self.writeVInt(0)
        self.writeVInt(2)
        self.writeBoolean(True)
        self.writeVInt(0)
        self.writeVInt(115)
        self.writeVInt(335442)
        self.writeVInt(1001442)
        self.writeVInt(5778642) 

        self.writeVInt(120)
        self.writeVInt(200)
        self.writeVInt(0)

        self.writeBoolean(True)
        self.writeVInt(2)
        self.writeVInt(2)
        self.writeVInt(2)
        self.writeVInt(0)
        self.writeVInt(0)

        ShopData = JSONHandler.ShopData

        self.writeVInt(len(ShopData["Offers"])) # Shop Offers

        for i in ShopData["Offers"]:
            def checkAvailability():
            	results = []
            	result = False
            	for reward in i["Rewards"]:
            		if reward["ItemType"] == 3 or reward["ItemType"] == 30:
            			if str(reward["BrawlerID"][1]) in list(player.OwnedBrawlers.keys()):
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 19:
            			if reward["Extra"] in player.OwnedPins or i["IsForPortalEvent"] == True and str(i["NeedsBrawler"]) not in player.OwnedBrawlers:
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 25:
            			if reward["Extra"] in player.OwnedThumbnails:
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 4:
            			if reward["Extra"] in player.OwnedSkins or i["IsForPortalEvent"] == True and str(i["NeedsBrawler"]) not in player.OwnedBrawlers:
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            	if i["Rewards"].index(reward) == len(i["Rewards"]) -1:
            		if True in results:
            			result = True
            	return result
            self.writeVInt(len(i["Rewards"]))
            for reward in i["Rewards"]:
                self.writeVInt(reward["ItemType"]) # ItemType
                self.writeVInt(reward["Amount"])
                if reward["BrawlerID"][0] != 0:
                    self.writeDataReference(reward["BrawlerID"][0], reward["BrawlerID"][1]) # CsvID
                else:
                    self.writeDataReference(0)
                self.writeVInt(reward["Extra"])
            self.writeVInt(i["Currency"])
            self.writeVInt(i["Cost"]) # new price
            self.writeVInt(i["Time"]) # timer until gone
            self.writeVInt(2)
            self.writeVInt(0)
            if ShopData["Offers"].index(i) in player.PurchasedOffers or checkAvailability() == True:
            	self.writeBoolean(True) # Claim
            else:
            	self.writeBoolean(i['Claim']) # Claim
            self.writeVInt(ShopData["Offers"].index(i))
            self.writeVInt(0)
            self.writeBoolean(False)
            self.writeVInt(i["OldPrice"]) # old price
            if i["Text"] == "None":
            	self.writeString()
            else:
            	self.writeString(i["Text"])
            self.writeVInt(0)
            self.writeBoolean(i["LoadOnStartup"])
            if i["Background"] == "None":
            	self.writeString()
            else:
            	self.writeString(i["Background"])
            self.writeVInt(-1)
            self.writeBoolean(i["Processed"])
            self.writeVInt(i["TypeBenefit"])
            self.writeVInt(i["Benefit"])
            self.writeString("")
            self.writeBoolean(i["OneTimeOffer"])
            self.writeBoolean(False)
            self.writeDataReference(i["ShopPanelLayout"][0], i["ShopPanelLayout"][1])
            self.writeDataReference(i["ShopStyleSet"][0], i["ShopStyleSet"][1]) #panel layout
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeVInt(i["OfferType"])
            self.writeVInt(-1)
            self.writeVInt(i["Cost"])
            self.writeBoolean(False) #шваль если тру то все офферы исчезают
            self.writeBoolean(True)
            self.writeVInt(6500)
            self.writeVInt(1929)
            self.writeBoolean(True)
        
        self.writeVInt(20)
        self.writeVInt(1428)

        self.writeVInt(0)

        self.writeVInt(1)
        self.writeVInt(30)

        self.writeByte(1) # count brawlers selected
        self.writeDataReference(16, player.SelectedBrawler) # selected brawler
        self.writeString(player.Region) # location
        self.writeString(player.ContentCreator) # supported creator

        self.writeVInt(6) 
        self.writeVInt(1) 
        self.writeVInt(9) 
        self.writeVInt(1) 
        self.writeVInt(22) 
        self.writeVInt(3) 
        self.writeVInt(25) 
        self.writeVInt(1) 
        self.writeVInt(24) 
        self.writeVInt(0)
        self.writeVInt(15)
        self.writeVInt(32447)
        self.writeVInt(28)


        self.writeVInt(0)

        self.writeVInt(1) # count brawl pass seasons
        self.writeVInt(20) # season
        self.writeVInt(900000) # season token collected
        self.writeBoolean(player.BrawlPassActive) # 0x1
        self.writeVInt(56)
        self.writeBoolean(False)
        self.writeBoolean(True) # 0x1
        self.writeInt(player.Pass32Int)
        self.writeInt(player.Pass64Int)
        self.writeInt(player.Pass96Int)
        self.writeInt(1)
        self.writeBoolean(True) # 0x0
        self.writeInt(player.Pass32IntP)
        self.writeInt(player.Pass64IntP)
        self.writeInt(player.Pass96IntP)
        self.writeInt(1)

        self.writeVInt(0)

        self.writeBoolean(True)
        self.writeVInt(0)
        self.writeVInt(1)
        self.writeVInt(2)
        self.writeVInt(0) 

        self.writeBoolean(True) # Vanity items
        self.writeVInt(ownedPinsCount + ownedThumbnailCount + ownedSprays)
        for i in player.OwnedPins:
            self.writeDataReference(52, i)
            self.writeVInt(1)
            for i in range(1):
                self.writeVInt(1)
                self.writeVInt(1)

        for i in player.OwnedThumbnails:
            self.writeDataReference(28, i)
            self.writeVInt(1)
            for i in range(1):
                self.writeVInt(1)
                self.writeVInt(1)  

        for i in player.OwnedSprays:
            self.writeDataReference(68, i)
            self.writeVInt(1)
            for i in range(1):
                self.writeVInt(1)
                self.writeVInt(1)  

        self.writeBoolean(False) # Power league season data

        self.writeInt(0)
        self.writeVInt(0)
        self.writeVInt(16)
        self.writeVInt(player.FavouriteBrawler)
        self.writeBoolean(False)

        self.writeVInt(2023189)

        self.writeVInt(35) # event slot id
        self.writeVInt(1)
        self.writeVInt(2)
        self.writeVInt(3)
        self.writeVInt(4)
        self.writeVInt(5)
        self.writeVInt(6)
        self.writeVInt(7)
        self.writeVInt(8)
        self.writeVInt(9)
        self.writeVInt(10)
        self.writeVInt(11)
        self.writeVInt(12)
        self.writeVInt(13) 
        self.writeVInt(14)
        self.writeVInt(15)
        self.writeVInt(16)
        self.writeVInt(17)
        self.writeVInt(18) 
        self.writeVInt(19)
        self.writeVInt(20)
        self.writeVInt(21) 
        self.writeVInt(22)
        self.writeVInt(23)
        self.writeVInt(24)
        self.writeVInt(25)
        self.writeVInt(26)
        self.writeVInt(27)
        self.writeVInt(28)
        self.writeVInt(29)
        self.writeVInt(30)
        self.writeVInt(31)
        self.writeVInt(32)
        self.writeVInt(33)
        self.writeVInt(34)
        self.writeVInt(35)

        self.writeVInt(1)

        self.writeVInt(1)
        self.writeVInt(1)
        self.writeVInt(1)
        self.writeVInt(0)
        self.writeVInt(72292)
        self.writeVInt(10) 
        self.writeDataReference(15, 7) # map id
        self.writeVInt(-1)
        self.writeVInt(2)
        self.writeString("")
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False) # MapMaker map structure array
        self.writeVInt(0)
        self.writeBoolean(False) # Power League array entry
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(-1)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(-1)
        self.writeVInt(0) 
        self.writeVInt(0) 
        self.writeVInt(0) 
        self.writeBoolean(False) 

        self.writeVInt(1)

        self.writeVInt(1)
        self.writeVInt(1)
        self.writeVInt(1)
        self.writeVInt(72292)
        self.writeVInt(72292)
        self.writeVInt(10) 
        self.writeDataReference(15, 7) # map id
        self.writeVInt(-1)
        self.writeVInt(2)
        self.writeString("")
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False) # MapMaker map structure array
        self.writeVInt(0)
        self.writeBoolean(False) # Power League array entry
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(-1)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(-1)
        self.writeVInt(0) 
        self.writeVInt(0) 
        self.writeVInt(0) 
        self.writeBoolean(False) 
       
        ByteStreamHelper.encodeIntList(self, [20, 35, 75, 140, 290, 480, 800, 1250, 1875, 2800])
        ByteStreamHelper.encodeIntList(self, [30, 80, 170, 360]) # Shop Coins Price
        ByteStreamHelper.encodeIntList(self, [300, 880, 2040, 4680]) # Shop Coins Amount

        self.writeVInt(0) 

        self.writeVInt(2)
        self.writeVInt(41000081) # theme
        self.writeVInt(1)
        self.writeVInt(1) 
        self.writeVInt(114) # camera

        self.writeVInt(0) 
        self.writeVInt(0)

        self.writeVInt(2)
        self.writeVInt(1)
        self.writeVInt(2)
        self.writeVInt(2)
        self.writeVInt(1)
        self.writeVInt(-1)
        self.writeVInt(2)
        self.writeVInt(1)
        self.writeVInt(4)

        ByteStreamHelper.encodeIntList(self, [0, 29, 79, 169, 349, 699])
        ByteStreamHelper.encodeIntList(self, [0, 160, 450, 500, 1250, 2500])

        self.writeLong(0, 1) # Player ID

        self.writeVInt(0) # Notification factory
        
        self.writeVInt(1)
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0) 
        self.writeVInt(0)
        self.writeBoolean(False) # Daily Login Calendar        
        self.writeVInt(0)
        self.writeBoolean(True) # Starr Road

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        
        if True:
            self.writeVInt(1)
        
            rare = [1, 2, 3, 6, 8, 10, 13, 24]
            super_rare = [7, 9, 18, 19, 22, 25, 27, 34, 61, 4]
            epic = [14, 15, 16, 20, 26, 29, 30, 36, 43, 45, 48, 50, 58, 69]
            mythic = [11, 17, 21, 35, 31, 32, 37, 42, 47, 64, 67, 71, 73]
            legendary = [5, 12, 23, 28, 40, 52, 63]
        
            x = player.RecruitBrawler
        
            self.writeDataReference(16, player.RecruitBrawler) 
            
            if x in rare:
                self.writeVInt(160)
            elif x in super_rare:
                self.writeVInt(430)
            elif x in epic:
                self.writeVInt(925)
            elif x in mythic:
               self.writeVInt(1900)
            elif x in legendary:
                self.writeVInt(3800)
            else:
                self.writeVInt(1)
            
            
            if x in rare:
                self.writeVInt(29)
            elif x in super_rare:
                self.writeVInt(79)
            elif x in epic:
                self.writeVInt(169)
            elif x in mythic:
                self.writeVInt(359)
            elif x in legendary:
                self.writeVInt(699)
            else:
                self.writeVInt(1)
            
            self.writeVInt(0)
            self.writeVInt(player.RecruitTokens) 
            self.writeVInt(0) 
            self.writeVInt(0)
        else:
        	self.writeVInt(0)
        
        
        self.writeVInt(len(player.Brawlers))
        for x in player.Brawlers:
            self.writeDataReference(16, x) 
                      
            
            if x in rare:
                self.writeVInt(160)
            elif x in super_rare:
                self.writeVInt(430)
            elif x in epic:
                self.writeVInt(925)
            elif x in mythic:
                self.writeVInt(1900)
            elif x in legendary:
                self.writeVInt(3800)
            else:
            	self.writeVInt(1)
            
            
            if x in rare:
                self.writeVInt(29)
            elif x in super_rare:
                self.writeVInt(79)
            elif x in epic:
                self.writeVInt(169)
            elif x in mythic:
                self.writeVInt(359)
            elif x in legendary:
                self.writeVInt(699)
            else:
            	self.writeVInt(1)
            
           
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(player.Brawlers.index(x)) 
            self.writeVInt(0)
        
        self.writeVInt(0)
        
        self.writeVInt(0)

        self.writeVInt(len(player.OwnedBrawlers)) # Mystery Brawl LakDev
        for brawlerID,brawlerInfo in player.OwnedBrawlers.items():           
            self.writeVInt(brawlerInfo["MasteryPoints"])
            self.writeVInt(brawlerInfo["MasteryTier"])
            self.writeDataReference(16, brawlerID)

        self.writeVInt(0)

        if player.BattleIcon1 == 0:
            self.writeVInt(0)
        else:
            self.writeDataReference(28, player.BattleIcon1) # icon

        if player.BattleIcon2 == 0:
            self.writeVInt(0)
        else:
            self.writeDataReference(28, player.BattleIcon2) # icon

        if player.BattleEmote == 0:
            self.writeVInt(0)
        else:
            self.writeDataReference(52, player.BattleEmote) # pin
        
        if player.Title == 0:
            self.writeVInt(0)
        else:
            self.writeDataReference(76, player.Title) # titles

        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeVInt(0) #Brawler's BattleCards

        starrDropOpening.encode(self, player)

        self.writeBoolean(False)


        self.writeVLong(player.ID[0], player.ID[1])
        self.writeVLong(player.ID[0], player.ID[1])
        self.writeVLong(player.ID[0], player.ID[1])
        self.writeStringReference(player.Name)
        self.writeBoolean(player.Registered)
        self.writeInt(-1)

        self.writeVInt(17)
        unlocked_brawler = [i['CardID'] for x,i in player.OwnedBrawlers.items()]
        self.writeVInt(len(unlocked_brawler) + 5)
        for x in unlocked_brawler:
            self.writeDataReference(23, x)
            self.writeVInt(-1)
            self.writeVInt(1)

        self.writeDataReference(5, 8)
        self.writeVInt(-1)
        self.writeVInt(player.Coins)

        self.writeDataReference(5, 18)
        self.writeVInt(-1)
        self.writeVInt(5)

        self.writeDataReference(5, 20)
        self.writeVInt(-1)
        self.writeVInt(player.ChromaticCoins) 

        self.writeDataReference(5, 22)
        self.writeVInt(-1)
        self.writeVInt(player.PowerPoints) 

        self.writeDataReference(5, 23)
        self.writeVInt(-1)
        self.writeVInt(player.Bling)

        self.writeVInt(len(player.OwnedBrawlers)) # HeroScore
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["Trophies"])

        self.writeVInt(len(player.OwnedBrawlers)) # HeroHighScore
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["HighestTrophies"])

        self.writeVInt(0) # Array

        self.writeVInt(0) # HeroPower
        
        self.writeVInt(len(player.OwnedBrawlers)) # HeroLevel
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(i["PowerLevel"]-1)

        self.writeVInt(0) # hero star power gadget and hypercharge

        self.writeVInt(len(player.OwnedBrawlers)) # HeroSeenState
        for x,i in player.OwnedBrawlers.items():
            self.writeDataReference(16, x)
            self.writeVInt(-1)
            self.writeVInt(2)

        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array
        self.writeVInt(0) # Array

        self.writeVInt(player.Gems) # Diamonds
        self.writeVInt(player.Gems) # Free Diamonds
        self.writeVInt(10) # Player Level
        self.writeVInt(100)
        self.writeVInt(0) # CumulativePurchasedDiamonds or Avatar User Level Tier | 10000 < Level Tier = 3 | 1000 < Level Tier = 2 | 0 < Level Tier = 1
        self.writeVInt(100) # Battle Count
        self.writeVInt(10) # WinCount
        self.writeVInt(80) # LoseCount
        self.writeVInt(50) # WinLooseStreak
        self.writeVInt(20) # NpcWinCount
        self.writeVInt(0) # NpcLoseCount
        self.writeVInt(2) # TutorialState | shouldGoToFirstTutorialBattle = State == 0
        self.writeVInt(12)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeString()
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(1)

    def decode(self):
        fields = {}
        return fields

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24101

    def getMessageVersion(self):
        return self.messageVLakDev 
