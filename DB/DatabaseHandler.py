import json
import sqlite3
import traceback
import time
from Heart.Files.Classes.Regions import Regions

class DatabaseHandler():
    def __init__(self):
        self.conn = sqlite3.connect("DB/Files/player.sqlite")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""CREATE TABLE main (ID int, Token text, Data json)""")
        except sqlite3.OperationalError:
            pass
        except Exception:
            print(traceback.format_exc())
    def fFriends(self):
        try:
            self.cursor.execute("SELECT ID, Data FROM main")
            rows = self.cursor.fetchall()
            for lowID, raw in rows:
                data = json.loads(raw)
                changed = False
                for friend in data["Friends"]:
                    if friend["Status"] == "pendingS":
                        friend["Status"] = 2
                        changed = True
                    elif friend["Status"] == "pendingA":
                        friend["Status"] = 3
                        changed = True
                    elif friend["Status"] == "friend":
                        friend["Status"] = 4
                        changed = True
                if changed:
                    self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(data, ensure_ascii=0), lowID))
            self.conn.commit()
        except Exception:
            print(traceback.format_exc())

    def AddFriend(self, ownerLow, friendLow, status=4):
        try:
            entry = self.cursor.execute("SELECT Data from main where ID=?", (ownerLow,)).fetchone()
            if entry is None:
                return
            data = json.loads(entry[0])
            friends = data["Friends"]
            if not any(f["IDLow"] == friendLow for f in friends):
                friends.append({"IDLow": friendLow, "Status": status})
            else:
                for f in friends:
                    if f["IDLow"] == friendLow:
                        f["Status"] = status
            data["Friends"] = friends
            self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(data, ensure_ascii=0), ownerLow))
            self.conn.commit()
        except Exception:
            print(traceback.format_exc())

    def DelFriend(self, ownerLow, friendLow):
        try:
            entry = self.cursor.execute("SELECT Data from main where ID=?", (ownerLow,)).fetchone()
            if entry is None:
                return
            data = json.loads(entry[0])
            data["Friends"] = [f for f in data["Friends"] if f["IDLow"] != friendLow]
            self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(data, ensure_ascii=0), ownerLow))
            self.conn.commit()
        except Exception:
            print(traceback.format_exc())

    def GetFriends(self, ownerLow):
        try:
            entry = self.cursor.execute("SELECT Data from main where ID=?", (ownerLow,)).fetchone()
            if entry is None:
                return []
            return json.loads(entry[0])["Friends"]
        except Exception:
            print(traceback.format_exc())
            return []

    def IsFriend(self, ownerLow, friendLow):
        try:
            entry = self.cursor.execute("SELECT Data from main where ID=?", (ownerLow,)).fetchone()
            if entry is None:
                return False
            friends = json.loads(entry[0])["Friends"]
            return any(f["IDLow"] == friendLow and f["Status"] == 4 for f in friends)
        except Exception:
            print(traceback.format_exc())
            return False

    def createAccount(self, data):
        try:
            self.cursor.execute("INSERT INTO main (ID, Token, Data) VALUES (?, ?, ?)", (data["ID"][1], data["Token"], json.dumps(data, ensure_ascii=0)))
            self.conn.commit()
        except Exception:
            print(traceback.format_exc())

    def getAll(self):
        self.playersId = []
        try:
            self.cursor.execute("SELECT * from main")
            self.db = self.cursor.fetchall()
            for i in range(len(self.db)):
                self.playersId.append(self.db[i][0])
            return self.playersId
        except Exception:
            print(traceback.format_exc())

    def load_all(self):
        self.ids = []
        try:
            self.cursor.execute("SELECT * from main")
            self.db = self.cursor.fetchall()
            for i in self.db:
                data_db = json.loads(i[2])
                self.ids.append(data_db)
            return self.ids
        except Exception:
            print(traceback.format_exc())

    def getPlayer(self, plrId):
        try:
            self.cursor.execute("SELECT * from main where ID=?", (plrId[1],))
            return json.loads(self.cursor.fetchall()[0][2])
        except Exception:
            print(traceback.format_exc())

    def getPlayerEntry(self, plrId):
        try:
            self.cursor.execute("SELECT * from main where ID=?", (plrId[1],))
            return self.cursor.fetchall()[0]
        except IndexError:
            pass
        except Exception:
            print(traceback.format_exc())


    def sLast(self, plrId):
        try:
            entry = self.getPlayerEntry(plrId)
            if entry is None:
                return
            data = json.loads(entry[2])
            data["LastOnline"] = int(time.time())
            self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(data, ensure_ascii=0), plrId[1]))
            self.conn.commit()
        except Exception:
            print(traceback.format_exc())

    def loadAccount(self, player, plrId):
        try:
            self.cursor.execute("SELECT * from main where ID=?", (plrId[1],))
            playerData = json.loads(self.cursor.fetchall()[0][2])
            changed = False
            for b in playerData["OwnedBrawlers"].values():
                if "StarPower" not in b:
                    b["StarPower"] = [23, 0]
                    changed = True
                if "Gadget" not in b:
                    b["Gadget"] = [23, 0]
                    changed = True
                if "Gear1" not in b:
                    b["Gear1"] = 0
                    changed = True
                if "Gear2" not in b:
                    b["Gear2"] = 0
                    changed = True
                if "Overcharge" not in b:
                    b["Overcharge"] = [0, 0]
                    changed = True
            if changed:
                self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(playerData, ensure_ascii=0), plrId[1]))
                self.conn.commit()
            player.ID = playerData["ID"]
            player.AllianceID = playerData["AllianceID"]
            player.HasClub = playerData["HasClub"]
            player.Name = playerData["Name"]
            player.Registered = playerData["Registered"]
            player.Thumbnail = playerData["Thumbnail"]
            player.Namecolor = playerData["Namecolor"]
            player.TeamID = playerData["TeamID"]
            player.Region = playerData["Region"]
            player.ContentCreator = playerData["ContentCreator"]
            player.Coins = playerData["Coins"]
            player.Gems = playerData["Gems"]
            player.RecruitTokens = playerData["RecruitTokens"]
            player.StarPoints = playerData["StarPoints"]            
            player.Trophies = playerData["Trophies"]
            player.HighestTrophies = playerData["HighestTrophies"]
            player.TrophyRoadTier = playerData["TrophyRoadTier"]
            player.Experience = playerData["Experience"]
            player.Level = playerData["Level"]
            player.Tokens = playerData["Tokens"]
            player.TokensDoubler = playerData["TokensDoubler"]
            player.SelectedBrawler = playerData["SelectedBrawler"]
            player.SelectedSkin = playerData["SelectedSkin"]
            player.OwnedPins = playerData["OwnedPins"]
            player.OwnedSprays = playerData["OwnedSprays"]
            player.SelectedSkins = playerData["SelectedSkins"]
            player.OwnedSkins = playerData["OwnedSkins"]
            player.OwnedThumbnails = playerData["OwnedThumbnails"]
            player.OwnedBrawlers = playerData["OwnedBrawlers"]
            player.OwnedTitles = playerData["OwnedTitles"]
            player.OwnedAccessories = playerData["OwnedAccessories"]
            player.ChromaticCoins = playerData["ChromaticCoins"]
            player.PowerPoints = playerData["PowerPoints"]
            player.Bling = playerData["Bling"]
            player.GatchaItems = playerData["GatchaItems"]
            player.PurchasedOffers = playerData["PurchasedOffers"]
            player.Pass32Int = playerData["Pass32Int"]
            player.Pass64Int = playerData["Pass64Int"]
            player.Pass96Int = playerData["Pass96Int"]
            player.Pass32IntP = playerData["Pass32IntP"]
            player.Pass64IntP = playerData["Pass64IntP"]
            player.Pass96IntP = playerData["Pass96IntP"]
            player.BrawlPassActive = playerData["BrawlPassActive"]
            player.RoadType = playerData["RoadType"]
            player.PassLevel = playerData["PassLevel"]
            player.PassSeason = playerData["PassSeason"]
            player.RecruitBrawler = playerData["RecruitBrawler"]
            player.RecruitCost = playerData["RecruitCost"]
            player.RecruitGemsCost = playerData["RecruitGemsCost"]
            player.RecruitBrawlerCard = playerData["RecruitBrawlerCard"]
            player.Brawlers = playerData["Brawlers"]
            player.BattleIcon1 = playerData["BattleIcon1"]
            player.BattleIcon2 = playerData["BattleIcon2"]
            player.BattleEmote = playerData["BattleEmote"]
            player.Title = playerData["Title"]
            player.BattleIcon1Visible = playerData["BattleIcon1Visible"]
            player.BattleIcon2Visible = playerData["BattleIcon2Visible"]
            player.BattleEmoteVisible = playerData["BattleEmoteVisible"]
            player.TitleVisible = playerData["TitleVisible"]
            player.FavouriteBrawler = playerData["FavouriteBrawler"]
            player.DropRarity = playerData["DropRarity"]
            player.DropAmount = playerData["DropAmount"]
            player.SeenNotifications = playerData["SeenNotifications"]
            player.Notifications = playerData["Notifications"]
            player.Quests = playerData["Quests"]
            player.ClaimedLoginRewardIndex = playerData["ClaimedLoginRewardIndex"]
            player.LoginRewardIndex = playerData["LoginRewardIndex"]
            player.DailyWins = playerData["DailyWins"]
            player.DailyFreebieItem = playerData["DailyFreebieItem"]
            player.DailyFreebieItemAmount = playerData["DailyFreebieItemAmount"]
            player.DailyFreebieClaimed = playerData["DailyFreebieClaimed"]
            player.Friends = playerData["Friends"] if "Friends" in playerData else []
            player.LastOnline = playerData["LastOnline"] if "LastOnline" in playerData else 0
        except Exception:
            print(traceback.format_exc())

    def updatePlayerData(self, data, calling_instance):
        try:
            self.cursor.execute("UPDATE main SET Data=? WHERE ID=?", (json.dumps(data, ensure_ascii=0), calling_instance.player.ID[1]))
            self.conn.commit()
            self.loadAccount(calling_instance.player, calling_instance.player.ID)
        except Exception:
            print(traceback.format_exc())

    def playerExist(self, loginToken, loginID):
        try:
            if loginID[1] in self.getAll():
                if loginToken != self.getPlayerEntry(loginID)[1]:
                    return False
                return True
            return False
        except Exception:
            print(traceback.format_exc())

    def getSorted(self):

        a = []

        self.cursor.execute("SELECT * FROM main")

        this = self.cursor.fetchall()

        for db in this:

            data = json.loads(db[2])

            a.append(data)

        a = sorted(a, key=lambda x:x["Trophies"], reverse=True)

        return a


class ClubDatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect("DB/Files/club.sqlite")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""CREATE TABLE main (LowID integer, Data json)""")
        except:
            pass

    def createClub(self, lowID, data):
        try:
            self.cursor.execute("INSERT INTO main (LowID, Data) VALUES (?, ?)",
                                (lowID, json.dumps(data, ensure_ascii=0)))
            self.conn.commit()
        except Exception as e:
            print(e)

    def deleteClub(self, lowID):
        try:
            self.cursor.execute("DELETE FROM main where LowID=?", (lowID,))
            self.conn.commit()
        except Exception as e:
            print(e)


    def getAllClub(self):
        clubs = []
        try:
            self.cursor.execute("SELECT * from main")
            self.db = self.cursor.fetchall()
            for i in range(len(self.db)):
                clubs.append(json.loads(self.db[i][1]))
            return clubs
        except Exception as e:
            print(e)

    def getAllClubByRegion(self, regionID):
        clubs = []
        try:
            self.cursor.execute("SELECT * from main")
            self.db = self.cursor.fetchall()
            for i in range(len(self.db)):
                dataLoaded = json.loads(self.db[i][1])
                if dataLoaded['RegionID'] == Regions.getIDByRegion(self, regionID):
                    clubs.append(dataLoaded)
            return clubs
        except Exception as e:
            print(traceback.format_exc())

    def getDefaultMembersData(self, player, role):
        return {'HighID': player.HighID, 'LowID': player.LowID, 'Name': player.Name, 'Role': role, 'Trophies': player.trophies, 'NameColor': player.nameColor, 'Thumbnail': player.thumbnail}

    def getDefaultMessageData(self, eventType, streamType, lastID, playerID, playerName, playerRole, target={}, msgData="", premadeID=-1, messageDataID=-1):
        return {'StreamType': eventType, 'EventType': streamType, 'StreamID': lastID, 'PlayerID': playerID, 'PlayerName': playerName, 'PlayerRole': playerRole, 'Message': msgData, 'Target': target, 'PremadeID': premadeID, 'MessageDataID': messageDataID}

    def getClubWithLowID(self, low):
        try:
            self.cursor.execute("SELECT * from main where LowID=?", (low,))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def getMembersSorted(self, clubdata):
        try:
            return sorted(clubdata['Members'].items(), key = lambda x: x[1]['Trophies'], reverse=True)
        except Exception as e:
            print(e)

    def getMemberWithLowID(self, clubData, playerLowID):
        try:
            return clubData["Members"][str(playerLowID)]
        except Exception as e:
            print(e)

    def getTotalTrophies(self, clubData):
        totalTrophies = 0
        for i in clubData["Members"].values():
            playerEntry = DatabaseHandler().getPlayerEntry([i["HighID"], i["LowID"]])
            if playerEntry is None:
                continue
            playerData = json.loads(playerEntry[2])
            totalTrophies += playerData.get("Trophies", 0)
        return totalTrophies

    def updateClubData(self, data, lowID):
        try:
            self.cursor.execute("UPDATE main SET Data=? WHERE LowID=?", (json.dumps(data, ensure_ascii=0), lowID))
            self.conn.commit()
        except Exception as e:
            print(e)

class TeamDatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect("DB/Files/team.sqlite")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""CREATE TABLE main (LowID integer, Data json)""")
        except:
            pass

    def createTeam(self, lowID, data):
        try:
            self.cursor.execute("INSERT INTO main (LowID, Data) VALUES (?, ?)",
                                (lowID, json.dumps(data, ensure_ascii=0)))
            self.conn.commit()
        except Exception as e:
            print(e)

    def deleteTeam(self, lowID):
        try:
            self.cursor.execute("DELETE FROM main where LowID=?", (lowID,))
            self.conn.commit()
        except Exception as e:
            print(e)

    def getAllTeam(self):
        teams = []
        try:
            self.cursor.execute("SELECT * from main")
            self.db = self.cursor.fetchall()
            for i in range(len(self.db)):
                teams.append(json.loads(self.db[i][1]))
            return teams
        except Exception as e:
            print(e)

    def getTeamWithLowID(self, low):
        try:
            self.cursor.execute("SELECT * from main where LowID=?", (low,))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def getMemberWithLowID(self, teamData, playerLowID):
        try:
            return teamData["Members"][str(playerLowID)]
        except Exception as e:
            print(e)

    def updateTeamData(self, data, lowID):
        try:
            self.cursor.execute("UPDATE main SET Data=? WHERE LowID=?", (json.dumps(data, ensure_ascii=0), lowID))
            self.conn.commit()
        except Exception as e:
            print(e)
