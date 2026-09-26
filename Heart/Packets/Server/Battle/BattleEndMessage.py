from Heart.Packets.PiranhaMessage import PiranhaMessage
from DB.DatabaseHandler import DatabaseHandler, ClubDatabaseHandler
import json

class BattleEndMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        calling_instance = fields["CallingInstance"]
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(player.ID)[2])
        self.writeLong(0, 0)
        self.writeLong(0, 0)

        self.writeVInt(fields["Unk1"])
        self.writeVInt(fields["Result"])
        self.writeVInt(0)
        self.writeVInt(8)
        mastery = 500
        fields["BrawlerID"] = next(h["Brawler"]["ID"][1] for h in fields["Heroes"] if h["IsPlayer"])
        player_data["Trophies"] += 8
        player_data["Experience"] += 1337
        player_data["OwnedBrawlers"][str(fields["BrawlerID"])]["Trophies"] += 8
        player_data["OwnedBrawlers"][str(fields["BrawlerID"])]["HighestTrophies"] += 8
        player_data["OwnedBrawlers"][str(fields["BrawlerID"])]["MasteryPoints"] += mastery
        db_instance.updatePlayerData(player_data, calling_instance)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(80085)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeBoolean(False)

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False) 
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeVInt(-1)
        self.writeBoolean(False)

        heroes = fields["Heroes"]
        self.writeVInt(len(heroes))

        for heroEntry in heroes:
            self.writeBoolean(bool(heroEntry["IsPlayer"]))
            self.writeBoolean(bool(heroEntry["Team"]))
            self.writeBoolean(bool(heroEntry["IsPlayer"])) #mvp

            self.writeVInt(1)
            self.writeDataReference(heroEntry["Brawler"]["ID"][0], heroEntry["Brawler"]["ID"][1])

            if heroEntry["Brawler"]["SkinID"] is None:
                self.writeVInt(0)
            else:
                self.writeVInt(1)
                self.writeDataReference(heroEntry["Brawler"]["SkinID"][0], heroEntry["Brawler"]["SkinID"][1])

            self.writeVInt(1) 
            self.writeVInt(0)

            self.writeVInt(1)
            self.writeVInt(5)

            self.writeVInt(1)
            self.writeVInt(0)

            self.writeVInt(0)
            self.writeVInt(0)

            if heroEntry["IsPlayer"]:
                self.writeBoolean(True)
                self.writeLong(player.ID[0], player.ID[1])
            else:
                self.writeBoolean(False)

            self.writeString(heroEntry["PlayerName"]) 
            self.writeVInt(100)
            self.writeVInt(28000000)
            self.writeVInt(43000000)
            self.writeVInt(-1)

            self.writeBoolean(False)
            self.writeVInt(1)
            self.writeVInt(player_data["OwnedBrawlers"][str(fields["BrawlerID"])]["MasteryPoints"]) # total
            self.writeVInt(1)
            self.writeVInt(mastery) # +
            self.writeInt16(0)
            self.writeInt16(0)
            self.writeInt(0)
            self.writeInt(0)
            self.writeDataReference(0, 0)

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeDataReference(0, 0)

        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeBoolean(False)
        self.writeVInt(0)

        self.writeBoolean(False)
        self.writeVInt(0)

        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeBoolean(False)
        self.writeBoolean(False)
        self.writeBoolean(False)

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 23456

    def getMessageVersion(self):
        return self.messageVersion