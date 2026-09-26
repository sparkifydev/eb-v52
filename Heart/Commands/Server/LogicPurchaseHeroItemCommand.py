from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
import json
import os

class LogicPurchaseHeroItemCommand(LogicCommand):
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
        cid = fields["CardID"]
        gems = fields["PayWithGems"]
        cards = json.load(open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/JSON/CsvToJson/Cards.json"))
        bid = None
        kind = None
        for e in cards:
            if cid in e["StarPowerCard"]:
                bid = e["Brawler"]
                kind = "StarPower"
                break
            if cid in e["GadgetCard"]:
                bid = e["Brawler"]
                kind = "Gadget"
                break
        if bid is None:
            return
        cost = 1000 if kind == "Gadget" else 2000
        db = DatabaseHandler()
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        bid = str(bid)
        if bid not in pd["OwnedBrawlers"]:
            return
        b = pd["OwnedBrawlers"][bid]
        if gems:
            if pd["Gems"] < cost // 10:
                return
            pd["Gems"] -= cost // 10
        else:
            if pd["Coins"] < cost:
                return
            pd["Coins"] -= cost
        b[kind] = [23, cid]
        db.updatePlayerData(pd, calling_instance)

    def getCommandType(self):
        return 557
