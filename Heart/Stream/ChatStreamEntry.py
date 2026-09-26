from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry


class ChatStreamEntry:
    def encode(self: ByteStream, info):
        StreamEntry.encode(self, info)
        self.writeString(info['Message'])
        self.writeBoolean(False)
