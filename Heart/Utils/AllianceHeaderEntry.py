from Heart.Files.Classes.Regions import Regions

class AllianceHeaderEntry:
    def encode(calling_instance, clubdb, clubData):
        calling_instance.writeLong(clubData["HighID"], clubData["LowID"])
        calling_instance.writeString(clubData["Name"])
        calling_instance.writeDataReference(8, clubData["BadgeID"])
        calling_instance.writeVInt(clubData["Type"])
        calling_instance.writeVInt(len(clubData["Members"]))
        calling_instance.writeVInt(clubdb.getTotalTrophies(clubData))
        calling_instance.writeVInt(clubData["TrophiesRequired"])
        calling_instance.writeDataReference(0)
        calling_instance.writeString(Regions.getRegionByID(calling_instance, 11))
        calling_instance.writeVInt(0)
        calling_instance.writeBoolean(clubData["FamilyFriendly"])
        calling_instance.writeVInt(29899859)
        calling_instance.writeVInt(1) # if not 0: 2 more vint (piggy state)
        calling_instance.writeVInt(0)
        calling_instance.writeVInt(1)
    
    def decode(calling_instance, fields):
        fields["AllianceHeaderEntry"] = {} # TODO: this thing
        return fields