from Heart.Record.ByteStream import ByteStream
from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json
import random


class LevelUpCommand(LogicCommand):
    
    def __init__(self, commandData):
        super().__init__(commandData)

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["BrawlerID"] = calling_instance.readDataReference()
        LogicCommand.parseFields(fields)
        return fields

    def encode(self, fields):
    	pass

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        brawler = fields["BrawlerID"][1]
        PL = 0
        for i,v in player_data["OwnedBrawlers"].items():
            if i == str(brawler):
                if v["PowerLevel"] == 1:
                	player_data["Coins"] -= 20
                	player_data["PowerPoints"] -= 20
                if v["PowerLevel"] == 2:
                	player_data["Coins"] -= 35
                	player_data["PowerPoints"] -= 30
                if v["PowerLevel"] == 3:
                	player_data["Coins"] -= 75
                	player_data["PowerPoints"] -= 50
                if v["PowerLevel"] == 4:
                	player_data["Coins"] -= 140
                	player_data["PowerPoints"] -= 80
                if v["PowerLevel"] == 5:
                	player_data["Coins"] -= 290
                	player_data["PowerPoints"] -= 130                	
                if v["PowerLevel"] == 6:
                	player_data["Coins"] -= 480
                	player_data["PowerPoints"] -= 210
                if v["PowerLevel"] == 7:
                	player_data["Coins"] -= 800
                	player_data["PowerPoints"] -= 340
                if v["PowerLevel"] == 8:
                	player_data["Coins"] -= 1250
                	player_data["PowerPoints"] -= 550
                if v["PowerLevel"] == 9:
                	player_data["Coins"] -= 1875
                	player_data["PowerPoints"] -= 890
                if v["PowerLevel"] == 10:
                	player_data["Coins"] -= 2800
                	player_data["PowerPoints"] -= 1440
                if v["PowerLevel"] != 12:
                	v["PowerLevel"] += 1
                PL = v["PowerLevel"]
        if PL != 12:
        	db_instance.updatePlayerData(player_data, calling_instance)


    def getCommandType(self):
        return 520



