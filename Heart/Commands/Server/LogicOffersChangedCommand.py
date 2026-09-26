from random import choice
import json
from Heart.Messaging import Messaging
from Heart.Commands.LogicServerCommand import LogicServerCommand
from Heart.Commands.LogicCommand import LogicCommand
from Database.DatabaseHandler import DatabaseHandler
from Heart.Messaging import Messaging
from Heart.Utils.Player import Player

from JSON.JSONHandler import JSONHandler

class LogicOffersChangedCommand(LogicServerCommand):
    def __init__(self, commandData):
        super().__init__(commandData)
    
    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        LogicCommand.parseFields(fields)
        return fields
        
    def encode(self, fields):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(fields["PlayerID"])[2])
        ShopData = JSONHandler.ShopData
        
        self.writeVInt(len(ShopData["Offers"])) # LogicShopData
        

        for i in ShopData["Offers"]:
            def checkAvailability():
            	results = []
            	result = False
            	for reward in i["Rewards"]:
            		if reward["ItemType"] == 3 or reward["ItemType"] == 30:
            			if str(reward["BrawlerID"][1]) in list(playerData["OwnedBrawlers"].keys()):
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 19:
            			if reward["Extra"] in playerData["OwnedPins"] or i["IsForPortalEvent"] == True and str(i["NeedsBrawler"]) not in playerData["OwnedBrawlers"]:
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 25:
            			if reward["Extra"] in playerData["OwnedThumbnails"]:
            				if len(i["Rewards"]) > 1:
            					results.append(True)
            				else:
            					result = True
            		if reward["ItemType"] == 4:
            			if reward["Extra"] in playerData["OwnedSkins"]:
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
            self.writeVInt(1)
            self.writeVInt(0)
            if ShopData["Offers"].index(i) in playerData["PurchasedOffers"] or checkAvailability() == True:
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
            self.writeVInt(0)
            self.writeVInt(-1)
            self.writeVInt(i["Cost"])
            self.writeBoolean(False)
            self.writeBoolean(False)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeBoolean(False)
        
      
        
        LogicServerCommand.encode(self, fields)
        return self.messagePayload
        
    def getCommandType(self):
        return 211
        
        