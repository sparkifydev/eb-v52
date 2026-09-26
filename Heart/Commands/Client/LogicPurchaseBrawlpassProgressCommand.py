from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json

class LogicPurchaseBrawlpassProgressCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields, player):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        fields["a"] = calling_instance.readVInt()
        fields["b"] = calling_instance.readVInt()
       
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])

        playerData["Gems"] -= 30

        Current = 18
        g = [_ for _ in range(71)]

        p = [0, 75, 150, 250, 400, 600, 900, 1300, 1700, 2100, 2500, 2900, 3300, 3700, 4100, 4500, 4900, 5300, 5700, 6100, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500, 14000, 14500, 15000, 15500, 16000, 16500, 17100, 17700, 18300, 18900, 19500, 20100, 20700, 21300, 21900, 22500, 23100, 23700, 24300, 24900, 25500, 26100, 26700, 27300, 27900, 28500, 29100, 29700, 30300, 30900, 31500, 32100, 32700, 33300, 33900, 34500]

        CurrentSeasonTokens = playerData["Tokens"] 

        GetTokens = [p[x+1]-CurrentSeasonTokens for x in range(len(g)) if p[x] <= CurrentSeasonTokens and p[x +1] > CurrentSeasonTokens][0]

        playerData["Tokens"] += GetTokens        
        db_instance.updatePlayerData(playerData, calling_instance)

    def getCommandType(self):
        return 536