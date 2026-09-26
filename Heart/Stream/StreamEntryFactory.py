from Heart.Stream.AllianceEventStreamEntry import AllianceEventStreamEntry
from Heart.Stream.ChatStreamEntry import ChatStreamEntry
from Heart.Stream.JoinRequestAllianceStreamEntry import JoinRequestAllianceStreamEntry
from Heart.Stream.MessageDataStreamEntry import MessageDataStreamEntry
from Heart.Stream.QuickChatStreamEntry import QuickChatStreamEntry
from Heart.Stream.ReplayStreamEntry import ReplayStreamEntry
from Heart.Stream.StreamEntry import StreamEntry
from Heart.Stream.TeamCreatedStreamEntry import TeamCreatedStreamEntry

StreamIDs = {
    2: ChatStreamEntry,
    3: JoinRequestAllianceStreamEntry,
    4: AllianceEventStreamEntry,
    5: ReplayStreamEntry,
    6: MessageDataStreamEntry,
    8: QuickChatStreamEntry,
    77: TeamCreatedStreamEntry,
}


class StreamEntryFactory:
    def encode(self, fields, info):
        streamID = info['StreamType']
        if streamID not in StreamIDs:
            raise NotImplementedError(f"Stream with id {streamID} is not implemented.")
        StreamIDs[streamID].encode(self, info)
