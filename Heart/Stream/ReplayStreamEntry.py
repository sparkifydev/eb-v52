from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry


class ReplayStreamEntry:
    def encode(self: ByteStream, info):
        StreamEntry.encode(self, info)
        self.writeVInt(0)
        self.writeLong(info['ReplayID'][0], info['ReplayID'][1])
        self.writeBoolean(False)
        self.writeString("String1")
        self.writeString("String2")
        self.writeString("String3")
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

