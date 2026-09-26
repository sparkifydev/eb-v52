from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json

class LogicPurchaseBrawlPassCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        fields["a"] = calling_instance.readVInt()
        fields["b"] = calling_instance.readVInt()
        fields["c"] = calling_instance.readVInt()
        fields["d"] = calling_instance.readVInt()
        fields["e"] = calling_instance.readVInt()
        fields["BP"] = calling_instance.readVInt()        
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        playerData["BrawlPassActive"] = True
        playerData["Gems"] -= 169
        db_instance.updatePlayerData(playerData, calling_instance)

    def getCommandType(self):
        return 534