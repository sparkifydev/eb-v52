from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json

class LogicSetPlayerFavouriteBrawlerCommand(LogicCommand):
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
        fields["BrawlerID"] = calling_instance.readVInt()
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        fields["Socket"] = calling_instance.client
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        
        player_data["FavouriteBrawler"] = fields["BrawlerID"]
        
        db_instance.updatePlayerData(player_data, calling_instance)

    def getCommandType(self):
        return 570