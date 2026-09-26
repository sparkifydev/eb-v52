from Heart.Stream.StreamEntry import StreamEntry


class QuickChatStreamEntry:
    def encode(self, info):
        StreamEntry.encode(self, info)
        self.writeDataReference(40, info["MessageDataID"])
        self.writeBoolean(False)
        self.writeString()
        self.writeVInt(0)
        self.writeVInt(info["PremadeID"])
