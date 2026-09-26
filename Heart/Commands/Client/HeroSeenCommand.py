import json

from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
from Heart.Record.ByteStream import ByteStream
import random


class HeroSeenCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        pass

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["BrawlerID"] = calling_instance.readDataReference()
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        brawler = fields["BrawlerID"][1]
        for i,v in player_data["OwnedBrawlers"].items():
            if i == str(brawler):
            	State = v["State"]
            	v["State"] = 2
        if State != 2:
        	db_instance.updatePlayerData(player_data, calling_instance)


    def getCommandType(self):
        return 522