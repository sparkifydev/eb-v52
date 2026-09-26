from Heart.ByteStream import ByteStream
from Heart.Stream.StreamEntry import StreamEntry

class MessageDataStreamEntry:
    def encode(self: ByteStream, info):
        StreamEntry.encode(self, info)
        self.writeDataReference(0, info['MessageID'])

