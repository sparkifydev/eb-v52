import json
from Heart.Commands.LogicCommand import LogicCommand
from DB.DatabaseHandler import DatabaseHandler


class LogicSelectSkinCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: fields["SelectedSkin"] = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: _ = calling_instance.readVInt()
        except: pass
        try: fields["SelectedBrawler"] = calling_instance.readDataReference()
        except: pass
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        if "SelectedSkin" not in fields:
            return
        db = DatabaseHandler()
        pd = json.loads(db.getPlayerEntry(calling_instance.player.ID)[2])
        sid = fields["SelectedSkin"]
        pd["SelectedSkin"] = sid
        if "SelectedBrawler" in fields:
            bid = fields["SelectedBrawler"][1]
            pd["SelectedBrawler"] = bid
            pd["SelectedSkins"][str(bid)] = sid
        db.updatePlayerData(pd, calling_instance)

    def getCommandType(self):
        return 506