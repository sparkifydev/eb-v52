from Heart.Commands.LogicServerCommand import LogicServerCommand
from DB.DatabaseHandler import DatabaseHandler
import json
from JSON.JSONHandler import JSONHandler
import random
from datetime import datetime

class LogicRefreshRandomRewardsCommand(LogicServerCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
                
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(fields["PlayerID"])[2])
        
        playerData["PurchasedOffers"].append(fields["Offer"])
        
        def RefreshValue():
        	return random.randint(1, 2500)
            
        try:
        	fields["StarrDrops"]
        except:
    	    fields["StarrDrops"] = False
        self.writeVInt(1)
        self.writeVInt(-1)
        self.writeVInt(-1)
        self.writeVLong(0, 1)
        self.writeVInt(1)
        self.writeVInt(5)
        for i in range(5):
            self.writeDataReference(80, i)
            self.writeVInt(-1)
            self.writeVInt(0)
        if fields["StarrDrops"] == True:
        	self.writeVInt(1)
        	for x in range(1):
        	   self.writeDataReference(80, fields["Rarity"])
        	   	
        	self.writeVInt(1)
        	for x in range(1):
        	      self.writeByte(1)
        	      self.writeVInt(5)
        	      self.writeVInt(1)
        	      self.writeDataReference(0)
        	      self.writeVInt(613)   
        else:
        	self.writeVInt(0)
        	self.writeVInt(0)
        self.writeInt(-1788180018)
        self.writeVInt(fields["Wins"]) # Battle Progression Step
        self.writeVInt(0)
        self.writeVInt(9393) # timer until refresh
        
        self.writeVInt(0)
        
        self.writeVInt(1)
        self.writeVInt(0)
        
        

        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        return LogicServerCommand.decode(calling_instance, fields)

    def getCommandType(self):
        return 228