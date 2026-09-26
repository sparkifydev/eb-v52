from Heart.Record.ByteStream import ByteStream
from Heart.Utils.ClientsManager import ClientsManager
from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler



class FriendSuggestionsMessage(PiranhaMessage):

    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0
        

    def encode(self, fields, cryptoInit):
        self.writeInt(1) # Friends Count
        
        self.writeInt(2000) # Games Played with
        self.writeLong(0, 0) # AccountID
        
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString()
        
        self.writeInt(999) # Trophies
        self.writeInt(0) # FriendState
        self.writeInt(0) # FriendReason
        self.writeInt(0) # Unk
        self.writeInt(0) # Array
        
        self.writeBoolean(False) # AllianceEntry
        
        
        self.writeString() # Unk
        self.writeInt(0) # LastOnlineTime
        self.writeInt(0) # PowerLeague
        self.writeBoolean(True) # PlayerDisplayData Boolean
        self.writeString("playertest")
        self.writeVInt(100)
        self.writeVInt(28000000 + 27)
        self.writeVInt(43000000 + 8)
        self.writeVInt(-1)
        
        self.writeInt(0)
        self.writeInt(0)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20199

    def getMessageVersion(self):
        return self.messageVersion
