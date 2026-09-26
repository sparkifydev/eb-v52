from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json

class LogicPurchaseHeroCardCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeVInt(0)
        self.writeBoolean(False)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["CardID"] = calling_instance.readVInt()
        fields["PayWithGems"] = calling_instance.readBoolean()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        cid = fields["CardID"]
        gems = fields["PayWithGems"]
        cost = 2000
        if gems:
            gpay = cost // 10
            if pd["Gems"] < gpay:
                return
            pd["Gems"] -= gpay
        else:
            if pd["Coins"] < cost:
                return
            pd["Coins"] -= cost
        for bid in pd["OwnedBrawlers"]:
            b = pd["OwnedBrawlers"][bid]
            if "Cards" not in b:
                b["Cards"] = []
            if cid not in b["Cards"]:
                b["Cards"].append(cid)
                break
        box = {"Type": 100, "Items": [{"Amount": 1, "DataRef": [23, cid], "RewardID": 4}]}
        pd["GatchaItems"] = {"Boxes": [box]}
        db.updatePlayerData(pd, calling_instance)
        fields["Socket"] = calling_instance.client
        fields["Command"] = {"ID": 203}
        fields["PlayerID"] = calling_instance.player.ID
        fields["StarrDrops"] = False
        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)

    def getCommandType(self):
        return 557
