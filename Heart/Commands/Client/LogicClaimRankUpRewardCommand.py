from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json
from Heart.Readers.CSVReaders.Milestones import Milestones
from Heart.Readers.CSVReaders.Pins import Emotes
from Heart.Readers.CSVReaders.Sprays import Sprays

import random
from JSON.JSONHandler import JSONHandler


class LogicClaimRankUpRewardCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields, player):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        calling_instance.readVInt()
        fields["RoadID"] = calling_instance.readVInt()
        fields["IsBrawler"] = calling_instance.readVInt()
        if fields["IsBrawler"] == 0:
            fields["Season"] = calling_instance.readVInt()
            fields["LVL"] = calling_instance.readVInt()
        else:
        	fields["Brawler"] = calling_instance.readVInt()
        	fields["Season"] = calling_instance.readVInt()
        	fields["LVL"] = calling_instance.readVInt()
        	
        	
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        fields["IsBrawlPassReward"] = True
        playerData["RoadType"] = fields['RoadID']
        playerData["PassLevel"] = fields['LVL'] + 2
        playerData["PassSeason"] = fields["Season"]              
        fields["Socket"] = calling_instance.client
        def encodeStarrDrop(amount):
        	randomDrop = random.randint(1, 15300)	
        	if randomDrop <= 4500:
        		a = JSONHandler.RareDropsData
        		fields["Rarity"] = 0
        	elif randomDrop <= 6500:
        		a = JSONHandler.SuperRareDropsData
        		fields["Rarity"] = 1
        	elif randomDrop <= 13500:
        		a = JSONHandler.EpicDropsData
        		fields["Rarity"] = 2
        	elif randomDrop <= 14500:
        		a = JSONHandler.MythicDropsData
        		fields["Rarity"] = 3
        	elif randomDrop <= 15300:
        		a = JSONHandler.LegendaryDropsData
        		fields["Rarity"] = 4       	
        	playerData["DropRarity"] = fields["Rarity"]
        	for i in a["DropsData"]:
        		item = random.choice(i["Items"])
        		ItemID = item["ItemID"]       			
        		Fallback = random.randint(item["MinFallback"], item["MaxFallback"])
        		DeliveryID = item["DeliveryID"]
        		DataRef = item["DataRef"]
        		if ItemID == "OwnedPins":
        			RandomItem = random.randint(52, 1000)
        		elif ItemID == "Spyrays":
        			RandomItem = random.randint(17, 191)
        		else:
        			RandomItem = random.randint(12, 100)
        	
        			
        	playerData["GatchaItems"] = {'Boxes': []}
        	box = {'Type': 0, 'Items': []}	
        	item = {'Amount': Fallback, 'DataRef': [DataRef, RandomItem],  'RewardID': DeliveryID}
        	box['Items'].append(item)
        	box['Type'] = 100
        	playerData["GatchaItems"]['Boxes'].append(box)
        	DeprecatedItems = ["OwnedPins", "OwnedThumbnails", "Spyrays"]
        	if ItemID not in DeprecatedItems:
        		SaveList = [] 
        		SaveList.append(Fallback)
        		playerData[ItemID] += SaveList[0]
        		SaveList.clear()
        	else:
        		SaveList = []
        		SaveList.append(RandomItem)
        		playerData[ItemID].append(SaveList[0])
        		SaveList.clear()	
        	playerData["DropAmount"] = amount
        	if amount == 1:
        		db_instance.updatePlayerData(playerData, calling_instance)
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 228}
        		fields["PlayerID"] = calling_instance.player.ID
        		fields["StarrDrops"] = True
        		fields["Offer"] = 99999
        		fields["Wins"] = playerData["DailyWins"]
        		Messaging.sendMessage(24111, fields, calling_instance.player, cryptoInit) 
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 203}
        		fields["StarrDrops"] = True
        		fields["PlayerID"] = calling_instance.player.ID
        		Messaging.sendMessage(24111, fields, calling_instance.player, cryptoInit)
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 228}
        		fields["PlayerID"] = calling_instance.player.ID
        		fields["StarrDrops"] = False
        		fields["Offer"] = 99999
        		fields["Wins"] = playerData["DailyWins"]
        		Messaging.sendMessage(24111, fields, calling_instance.player, cryptoInit)
        
        if fields["LVL"] < 30 and fields["RoadID"] == 10:
            playerData["Pass32IntP"] += (2**(fields["LVL"]+2))
        elif fields["LVL"] >= 30 and fields["LVL"] <= 61 and fields["RoadID"] == 10:
            playerData["Pass64IntP"] += (2**(fields["LVL"] - 30))
        elif fields["LVL"] == 62 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 1
        elif fields["LVL"] == 63 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 2
        elif fields["LVL"] == 64 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 4
        elif fields["LVL"] == 65 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 8
        elif fields["LVL"] == 66 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 16
        elif fields["LVL"] == 67 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 32
        elif fields["LVL"] == 68 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 64
        elif fields["LVL"] == 69 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 128
        elif fields["LVL"] == 70 and fields["RoadID"] == 10:
            playerData["Pass96IntP"] += 256
        
            
        elif fields["LVL"] < 30 and fields["RoadID"] == 9:
            playerData["Pass32Int"] += (2**(fields["LVL"]+2))                                            
        elif fields["LVL"] >= 30 and fields["LVL"] <= 61 and fields["RoadID"] == 9:
            playerData["Pass64Int"] += (2**(fields["LVL"] - 30))
        elif fields["LVL"] == 62 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 1
        elif fields["LVL"] == 63 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 2
        elif fields["LVL"] == 64 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 4
        elif fields["LVL"] == 65 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 8
        elif fields["LVL"] == 66 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 16
        elif fields["LVL"] == 67 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 32
        elif fields["LVL"] == 68 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 64
        elif fields["LVL"] == 69 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 128
        elif fields["LVL"] == 70 and fields["RoadID"] == 9:
            playerData["Pass96Int"] += 256
        
        
        if fields['RoadID'] == 9 or fields['RoadID'] == 10:
            MilestoneReader = Milestones.getBrawlPassLvl(fields['RoadID'], fields['Season'], fields['LVL'])
            CountReward = MilestoneReader['PrimaryLvlUpRewardCount']           

            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 1:
                RewardID = 7
                CsvID = 0
                CsvID1 = 0
                playerData["Coins"] += int(CountReward)
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 49:
                RewardID = 7
                CsvID = 0
                CsvID1 = 0
                encodeStarrDrop(1)
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 3:
                if "70" in playerData["OwnedBrawlers"]:
                	RewardID = 7
                	CsvID = 0
                	CsvID1 = 0
                	CountReward = 50
                	playerData["Coins"] += 50
                else:
                	RewardID = 1
                	CsvID = 16
                	CsvID1 = 74
                	playerData["OwnedBrawlers"][74] = {'CardID': 619, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'MasteryPoints': 0, 'MasteryTier': 0, 'State': 2}
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 4:
                if 728 in playerData["OwnedSkins"]:
                	RewardID = 7
                	CsvID = 0
                	CsvID1 = 0
                	CountReward = 50
                	playerData["Coins"] += 50
                else:
                	RewardID = 9
                	CsvID = 29
                	CsvID1 = 728
                	playerData["OwnedSkins"].append(728)
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 25:
                RewardID = 11
                CsvID = 28
                CsvID1 = 330
                playerData["OwnedThumbnails"].append(330)
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 19:
                CsvID1 = Emotes.getEmoteIdByName(MilestoneReader['PrimaryLvlUpRewardData'])
                if CsvID1 in playerData["OwnedPins"]:
                	RewardID = 7
                	CsvID = 0
                	CountReward = 50
                	playerData["Coins"] += CountReward
                else:
                	RewardID = 11
                	CsvID = 52
                	playerData["OwnedPins"].append(int(CsvID1))

            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 35:
                CsvID1 = Sprays.getEmoteIdByName(MilestoneReader['PrimaryLvlUpRewardData'])
                if CsvID1 in playerData["OwnedSprays"]:
                	RewardID = 7
                	CsvID = 0
                	CountReward = 50
                	playerData["Coins"] += CountReward
                else:
                	RewardID = 11
                	CsvID = 68
                	playerData["OwnedSprays"].append(int(CsvID1))
                
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 16:
                RewardID = 8
                CsvID = 0
                CsvID1 = 0
                playerData["Gems"] += int(CountReward)
            
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 38:
                RewardID = 22
                CsvID = 0
                CsvID1 = 0
                playerData["RecruitTokens"] += int(CountReward)
            
            
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 39:
                RewardID = 23
                CsvID = 0
                CsvID1 = 0
                playerData["ChromaticCoins"] += int(CountReward)
            
            
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 41:
                RewardID = 24
                CsvID = 0
                CsvID1 = 0
                playerData["PowerPoints"] += int(CountReward)
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 45:
                RewardID = 25
                CsvID = 0
                CsvID1 = 0
                playerData["Bling"] += int(CountReward)
            
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 43:
                RewardID = 11
                CsvID = 76
                CsvID1 = 73 
                playerData["OwnedTitles"].append(73)
                
        if fields['RoadID'] == 10:
            db_instance.updatePlayerData(playerData, calling_instance)
            playerData["GatchaItems"] = {'Boxes': []}
            box = {'Type': 0, 'Items': []}
            item = {'Amount': CountReward, 'DataRef': [CsvID, CsvID1], 'RewardID': RewardID}
            box['Items'].append(item)
            box['Type'] = 100
            playerData["GatchaItems"]['Boxes'].append(box)
            db_instance.updatePlayerData(playerData, calling_instance)
            fields["Socket"] = calling_instance.client
            fields["Command"] = {"ID": 203}
            fields["PlayerID"] = calling_instance.player.ID
            Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
            
        print(fields["RoadID"])
                
        if fields['RoadID'] == 9:
            db_instance.updatePlayerData(playerData, calling_instance)
            playerData["GatchaItems"] = {'Boxes': []}
            box = {'Type': 0, 'Items': []}
            item = {'Amount': CountReward, 'DataRef': [CsvID, CsvID1], 'RewardID': RewardID}
            box['Items'].append(item)
            box['Type'] = 100
            playerData["GatchaItems"]['Boxes'].append(box)
            db_instance.updatePlayerData(playerData, calling_instance)
            fields["Socket"] = calling_instance.client
            fields["Command"] = {"ID": 203}
            fields["PlayerID"] = calling_instance.player.ID
            Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
            
        if fields['RoadID'] == 6:
            MilestoneReader = Milestones.getTrophyRoadLvL(fields['LVL'])
            CountReward = MilestoneReader['PrimaryLvlUpRewardCount']
            if int(MilestoneReader['PrimaryLvlUpRewardType']) == 1:
                RewardID = 7
                ItemID = "Coins"
            elif int(MilestoneReader['PrimaryLvlUpRewardType']) == 16:
                RewardID = 8
                ItemID = "Gems"
            elif int(MilestoneReader['PrimaryLvlUpRewardType']) == 38:
                RewardID = 22
                ItemID = "RecruitTokens"
            elif int(MilestoneReader['PrimaryLvlUpRewardType']) == 41:
                RewardID = 24
                ItemID = "PowerPoints"
            elif int(MilestoneReader['PrimaryLvlUpRewardType']) == 45:
                RewardID = 25
                ItemID = "Bling"
            else:
                RewardID = 50
                ItemID = "Coins"
                CountReward = 0
            playerData["TrophyRoadTier"] += 1
            playerData[ItemID] += int(CountReward)
            playerData["GatchaItems"] = {'Boxes': []}
            box = {'Type': 100, 'Items': []}
            item = {'Amount': CountReward, 'DataRef': [0, 0], 'RewardID': RewardID}
            box['Items'].append(item)
            playerData["GatchaItems"]['Boxes'].append(box)
            db_instance.updatePlayerData(playerData, calling_instance)
            fields["Socket"] = calling_instance.client
            fields["Command"] = {"ID": 203}
            fields["PlayerID"] = calling_instance.player.ID
            Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)

    def getCommandType(self):
        return 517