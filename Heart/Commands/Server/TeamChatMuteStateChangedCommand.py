from Heart.Commands.LogicCommand import LogicCommand


class TeamChatMuteStateChangedCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeBoolean(False)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["Muted"] = calling_instance.readBoolean()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        pass

    def getCommandType(self):
        return 221
