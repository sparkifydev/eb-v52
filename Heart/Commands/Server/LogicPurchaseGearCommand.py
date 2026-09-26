from Heart.Commands.LogicCommand import LogicCommand
from DB.DatabaseHandler import DatabaseHandler
import json

class LogicPurchaseGearCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeDataReference(0)
        self.writeDataReference(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["Character"] = calling_instance.readDataReference()
        fields["Gear"] = calling_instance.readDataReference()
        fields["Slot"] = calling_instance.readVInt()
        fields["PayWithGems"] = calling_instance.readBoolean()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db = DatabaseHandler()
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        ch = fields["Character"]
        gr = fields["Gear"]
        gems = fields["PayWithGems"]
        if not ch or not ch[0] or not gr or not gr[0]:
            return
        bid = str(ch[1])
        gid = gr[1]
        cost = 1000
        if gems:
            gpay = cost // 10
            if pd["Gems"] < gpay:
                return
            pd["Gems"] -= gpay
        else:
            if pd["Coins"] < cost:
                return
            pd["Coins"] -= cost
        if bid not in pd["OwnedBrawlers"]:
            return
        b = pd["OwnedBrawlers"][bid]
        slot = fields["Slot"]
        if slot == 2:
            b["Gear2"] = gid
        else:
            b["Gear1"] = gid
        db.updatePlayerData(pd, calling_instance)

    def getCommandType(self):
        return 558
