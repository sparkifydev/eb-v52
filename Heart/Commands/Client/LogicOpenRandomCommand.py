from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging

import json
import random

from JSON.JSONHandler import JSONHandler
from DB.DatabaseHandler import DatabaseHandler

class LogicOpenRandomCommand(LogicCommand):
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
        fields["Unk1"] = calling_instance.readVInt()
        fields["RewardType"] = calling_instance.readVInt()
        fields["RewardAmount"] = calling_instance.readVInt()
        fields["Unk2"] = calling_instance.readVInt()
        fields["Unk3"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        fields["IsBrawlPassReward"] = False
        
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        
        def getRandomValue():
        	return random.randint(1, 2250)
        
        
        def encodeStarrDrop(rarity):
        	if rarity == 0:
        		a = JSONHandler.RareDropsData
        		fields["Rarity"] = 0
        	elif rarity == 1:
        		a = JSONHandler.SuperRareDropsData
        		fields["Rarity"] = 1
        	elif rarity == 2:
        		a = JSONHandler.EpicDropsData
        		fields["Rarity"] = 2
        	elif rarity == 3:
        		a = JSONHandler.MythicDropsData
        		fields["Rarity"] = 3
        	elif rarity == 4:
        		a = JSONHandler.LegendaryDropsData
        		fields["Rarity"] = 4
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
        		SaveList = [] # лист для сохры рандом результата
        		SaveList.append(Fallback) # один рандом результат идет туда
        		playerData[ItemID] += SaveList[0] # добавление первого элемента листа к сумме валюты
        		SaveList.clear() # очистка листа для следующей работы
        	else:
        		SaveList = []
        		SaveList.append(RandomItem)
        		playerData[ItemID].append(SaveList[0])
        		SaveList.clear()
        	playerData["DropAmount"] -= 1	
        	if True:
        		db_instance.updatePlayerData(playerData, calling_instance)
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 228}
        		fields["PlayerID"] = calling_instance.player.ID
        		fields["StarrDrops"] = True
        		fields["Offer"] = 9999
        		fields["Wins"] = playerData["DailyWins"]
        		Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player) 
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 203}
        		fields["StarrDrops"] = True
        		fields["PlayerID"] = calling_instance.player.ID
        		Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
        	if playerData["DropAmount"] == 0:
        		fields["Socket"] = calling_instance.client
        		fields["Command"] = {"ID": 228}
        		fields["PlayerID"] = calling_instance.player.ID
        		fields["StarrDrops"] = False
        		fields["Wins"] = playerData["DailyWins"]
        		fields["Offer"] = 9999       		
        		Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
        		playerData["DropRarity"] = 0
        	
        encodeStarrDrop(playerData["DropRarity"])

    def getCommandType(self):
        return 571