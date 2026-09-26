from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from Heart.Logic.LogicStarrDropData import starrDropOpening
from DB.DatabaseHandler import DatabaseHandler

from Heart.Readers.CSVReaders.Skins import Skins
from Heart.Readers.CSVReaders.Pins import Emotes
from Heart.Readers.CSVReaders.PlayerThumbnails import PlayerThumbnails
from Heart.Readers.CSVReaders.Sprays import Sprays

from Heart.Readers.JSONReaders.Cards import CardFetcher

import json
import random

from JSON.JSONHandler import JSONHandler

class PurchaseOfferCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeVInt(0)
        self.writeDataReference(0)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["OfferIndex"] = calling_instance.readVInt()
        fields["PurchasedItem"] = calling_instance.readDataReference()
        fields["Unk"] = calling_instance.readDataReference()
        fields["CurrencySlot"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)

        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        
        fields["IsBrawlPassReward"] = False
        
        ShopData = JSONHandler.ShopData
        
        
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        
        
        def getRandomValue():
        	return random.randint(1, 2250)
        	
		
        		
        box = {'Type': 100, 'Items': []}
        boxVanity = {'Type': 100, 'Items': []}
        
        
        def giveDeliveryResources(type, amount):
        	playerData[type] += amount
        	if type == "Coins":
        		boxType = 7
        	if type == "Gems":
        		boxType = 8
        	if type == "Bling":
        		boxType = 25
        	if type == "RecruitTokens":
        		boxType = 22
        	if type == "ChromaticCoins":
        		boxType = 23
        	if type == "PowerPoints":
        		boxType = 24
        	playerData["GatchaItems"] = {'Boxes': []}	
        	item = {'Amount': amount, 'DataRef': [0, 0],  'RewardID': boxType}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)
        	
        
        def giveDeliveryVanity(type, amount, skin):
        	playerData[type].append(skin)
        	if type == "OwnedPins":
        		boxType = 52
        	if type == "OwnedThumbnails":
        		boxType = 28
        	if type == "OwnedSprays":
        		boxType = 68
        	playerData["GatchaItems"] = {'Boxes': []}
        		
        	item = {'Amount': amount, 'DataRef': [boxType, skin],  'RewardID': 11}
        	boxVanity['Items'].append(item)
        	if len(box["Items"]) != 0:
        		playerData["GatchaItems"]['Boxes'].append(box)
        	playerData["GatchaItems"]['Boxes'].append(boxVanity)
        	
        	
        def giveDeliverySkin(skin):
        	playerData["OwnedSkins"].append(skin)
        	playerData["GatchaItems"] = {'Boxes': []}	
        	item = {'Amount': 1, 'DataRef': [29, skin],  'RewardID': 9}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)

        def giveDeliveryBrawler(brawler, card, powerlevel):
        	playerData["OwnedBrawlers"][brawler] = {'CardID': card, 'Skins': [0], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': powerlevel, 'PowerPoints': 0, 'State': 2, 'MasteryPoints': 0, 'MasteryTier': 0}
        	playerData["GatchaItems"] = {'Boxes': []}	
        	item = {'Amount': 1, 'DataRef': [16, brawler],  'RewardID': 1}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)

        def giveDeliveryAccessory(acc):
        	for bid in playerData["OwnedBrawlers"]:
        		b = playerData["OwnedBrawlers"][bid]
        		if "Cards" not in b:
        			b["Cards"] = []
        		if acc not in b["Cards"]:
        			b["Cards"].append(acc)
        			break
        	playerData["GatchaItems"] = {'Boxes': []}
        	item = {'Amount': 1, 'DataRef': [23, acc], 'RewardID': 4}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)

        def giveDeliveryGear(gid):
        	for bid in playerData["OwnedBrawlers"]:
        		b = playerData["OwnedBrawlers"][bid]
        		if "Gears" not in b:
        			b["Gears"] = []
        		if gid not in b["Gears"]:
        			b["Gears"].append(gid)
        			break
        	playerData["GatchaItems"] = {'Boxes': []}
        	item = {'Amount': 1, 'DataRef': [62, gid], 'RewardID': 25}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)

        def giveDeliveryOvercharge(oid):
        	for bid in playerData["OwnedBrawlers"]:
        		b = playerData["OwnedBrawlers"][bid]
        		b["Overcharge"] = oid
        		break
        	playerData["GatchaItems"] = {'Boxes': []}
        	item = {'Amount': 1, 'DataRef': [23, oid], 'RewardID': 26}
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)
        	
        	
        def changeResourceNegative(resource, amount):
        	playerData[resource] -= amount
        	
        	        
        def sendCommand(command):
        	db_instance.updatePlayerData(playerData, calling_instance)
        	if command == 203:
        		fields["StarrDrops"] = False
        	else:
        		pass
        	fields["Socket"] = calling_instance.client
        	fields["Command"] = {"ID": command}
        	fields["PlayerID"] = calling_instance.player.ID
        	Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)      
        
	     
        	
        def clearBox():
        	box['Items'].clear()
        	boxVanity['Items'].clear()
        	
        	
        def specializeResource(intType, amount):
        	if intType == 1:
        		resource = "Coins"
        	elif intType == 16:
        		resource = "Gems"
        	elif intType == 45:
        		resource = "Bling"
        	elif intType == 38:
        		resource = "RecruitTokens"
        	elif intType == 39:
        		resource = "ChromaticCoins"
        	elif intType == 41:
        		resource = "PowerPoints"
        	giveDeliveryResources(resource, amount)
        	
        
        def specializeVanity(intType, amount, extra):
        	if intType == 19:
        		vanity = "OwnedPins"
        	elif intType == 25:
        		vanity = "OwnedThumbnails"
        	elif intType == 35:
        		vanity = "OwnedSprays"
        	giveDeliveryVanity(vanity, amount, extra)
        	
        if fields["OfferIndex"] == 0:
        	if playerData["DailyFreebieClaimed"] == False:
        		specializeResource(playerData["DailyFreebieItem"], playerData["DailyFreebieItemAmount"])
        		claimDailyFreebie()
        		sendCommand(203)
        		clearBox()
        	else:
        		pass
        	
        for i in ShopData["Offers"]:
        	if fields["OfferIndex"] == ShopData["Offers"].index(i) + 1 and fields["OfferIndex"] != 1250:
        		AppendableItems = [25, 19, 35]
        		for reward in i["Rewards"]:
        			DropRarity = reward["Extra"]
        			if reward["ItemType"] in AppendableItems:
        				specializeVanity(reward["ItemType"], 1, reward["Extra"])
        			
        			elif reward["ItemType"] == 3:
        				BrawlerCard = CardFetcher.fetchBrawlerCard(reward["BrawlerID"][1])
        				giveDeliveryBrawler(reward["BrawlerID"][1], int(BrawlerCard["CardID"]), reward["BrawlerPower"])
        			elif reward["ItemType"] == 4:
        				giveDeliverySkin(reward["Extra"])
        			elif reward["ItemType"] == 5:
        				giveDeliveryAccessory(reward["Extra"])
        			if fields["OfferIndex"] == 0:
        				playerData["PurchasedOffers"].append(0)
        			else:
        				playerData["PurchasedOffers"].append(ShopData["Offers"].index(i))
        		if i["Currency"] == 0:
        			changeResourceNegative("Gems", i["Cost"])
        		elif i["Currency"] == 1:
        			changeResourceNegative("Coins", i["Cost"])
        		elif i["Currency"] == 3:
        			changeResourceNegative("Bling", i["Cost"])
        		else:
        			pass
        		if i["StarrDrops"] == True:
        			clearBox()
        		elif i["UpdateOffers"] == True:
        			sendCommand(203)
        			sendCommand(211)
        			clearBox()
        		else:
        			sendCommand(203)
        			clearBox()

        if fields["OfferIndex"] == 42:
        	giveDeliveryAccessory(613)
        	sendCommand(203)
        	clearBox()

        
        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 29:
        	giveDeliverySkin(fields["PurchasedItem"][1])
        	SkinData = Skins.getCostSkinByID(fields["PurchasedItem"][1])
        	print(SkinData)
        	if fields["CurrencySlot"] == 1:
        		changeResourceNegative("Gems", int(SkinData["Diamonds"]))
        	if fields["CurrencySlot"] == 2:
        		changeResourceNegative("Bling", int(SkinData["Bling"]))
        	sendCommand(203)
        	clearBox()
        	
        
        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 52:

        	giveDeliveryVanity("OwnedPins", 1, fields["PurchasedItem"][1])
        	EmoteData = Emotes.getCostPinsByID(fields["PurchasedItem"][1])
        	print(EmoteData)
        	if fields["CurrencySlot"] == 1:
        		changeResourceNegative("Gems", int(EmoteData["Diamonds"]))
        	if fields["CurrencySlot"] == 2:
        		changeResourceNegative("Bling", int(EmoteData["Bling"]))
        	sendCommand(203)
        	clearBox()
        
        
        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 28:
        	giveDeliveryVanity("OwnedThumbnails", 1, fields["PurchasedItem"][1])
        	ThumbnailData = PlayerThumbnails.getCostThumbnailsByID(fields["PurchasedItem"][1])
        	if fields["CurrencySlot"] == 1:
        		changeResourceNegative("Gems", int(ThumbnailData["Diamonds"]))
        	if fields["CurrencySlot"] == 2:
        		changeResourceNegative("Bling", int(ThumbnailData["Bling"]))
        	sendCommand(203)
        	clearBox()

        
        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 68:
        	giveDeliveryVanity("OwnedSprays", 1, fields["PurchasedItem"][1])
        	SprayData = Sprays.getCostSprayByID(fields["PurchasedItem"][1])
        	if fields["CurrencySlot"] == 1:
        		changeResourceNegative("Gems", int(SprayData["Diamonds"]))
        	if fields["CurrencySlot"] == 2:
        		changeResourceNegative("Bling", int(SprayData["Bling"]))
        	sendCommand(203)
        	clearBox()

        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 23:
        	iid = fields["PurchasedItem"][1]
        	cost = 2000
        	if fields["CurrencySlot"] == 1:
        		gpay = cost // 10
        		if playerData["Gems"] < gpay:
        			return
        		changeResourceNegative("Gems", gpay)
        	elif fields["CurrencySlot"] == 0:
        		if playerData["Coins"] < cost:
        			return
        		changeResourceNegative("Coins", cost)
        	else:
        		gpay = fields["CurrencySlot"]
        		if gpay < 0:
        			gpay = 0
        		need = cost - gpay * 10
        		if need < 0:
        			need = 0
        		if playerData["Gems"] < gpay or playerData["Coins"] < need:
        			return
        		changeResourceNegative("Gems", gpay)
        		changeResourceNegative("Coins", need)
        	giveDeliveryAccessory(iid)
        	sendCommand(203)
        	clearBox()

        if fields["PurchasedItem"] is not None and fields["PurchasedItem"][0] == 62:
        	iid = fields["PurchasedItem"][1]
        	cost = 1000
        	if fields["CurrencySlot"] == 1:
        		gpay = cost // 10
        		if playerData["Gems"] < gpay:
        			return
        		changeResourceNegative("Gems", gpay)
        	elif fields["CurrencySlot"] == 0:
        		if playerData["Coins"] < cost:
        			return
        		changeResourceNegative("Coins", cost)
        	else:
        		gpay = fields["CurrencySlot"]
        		if gpay < 0:
        			gpay = 0
        		need = cost - gpay * 10
        		if need < 0:
        			need = 0
        		if playerData["Gems"] < gpay or playerData["Coins"] < need:
        			return
        		changeResourceNegative("Gems", gpay)
        		changeResourceNegative("Coins", need)
        	giveDeliveryGear(iid)
        	sendCommand(203)
        	clearBox()

    def getCommandType(self):
        return 519
