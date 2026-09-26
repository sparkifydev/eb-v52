from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler

class LogicSetPlayerBattleCardCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["Unk1"] = calling_instance.readVInt() # dark shit
        fields["CsvID"] = calling_instance.readVInt()
        fields["VanityID"] = calling_instance.readVInt()      
        fields["SlotID"] = calling_instance.readVInt()
        if fields["CsvID"] != 0:
            fields["Index"] = calling_instance.readVInt()
        else:
        	fields["Index"] = calling_instance.readBoolean()  
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = db_instance.getPlayer(calling_instance.player.ID)
        if fields["CsvID"] == 28 and fields["Index"] == 0:
        	playerData["BattleIcon1"] = fields["VanityID"]
        	playerData['BattleIcon1Visible'] = True
        if fields["CsvID"] == 28 and fields["Index"] == 1:
        	playerData["BattleIcon2"] = fields["VanityID"]
        	playerData['BattleIcon2Visible'] = True
        if fields["CsvID"] == 52:
        	playerData["BattleEmote"] = fields["VanityID"]
        	playerData['BattleEmoteVisible'] = True
        if fields["CsvID"] == 76:
        	playerData["Title"] = fields["VanityID"]
        	playerData['TitleVisible'] = True
        if fields["Index"] == True and fields["SlotID"] == 0:
        	playerData["BattleIcon1Visible"] = False
        if fields["Index"] == True and fields["SlotID"] == 1:
        	playerData["BattleIcon2Visible"] = False
        if fields["Index"] == True and fields["SlotID"] == 5:
        	playerData["BattleEmoteVisibke"] = False
        if fields["Index"] == True and fields["SlotID"] == 10:
        	playerData["TitleVisible"] = False
        db_instance.updatePlayerData(playerData, calling_instance)

    def getCommandType(self):
        return 568