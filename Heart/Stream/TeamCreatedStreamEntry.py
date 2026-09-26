from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry


class TeamCreatedStreamEntry:
    def encode(self: ByteStream, info):
        StreamEntry.encode(self, info)
        self.writeVLong(info["TargetID"][0], info["TargetID"][1])
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
