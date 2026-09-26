import json
import random
import string

from datetime import date
today = date.today()
daily_freebie_items = [45, 1, 41, 38]

class Player:
    ClientVersion = "0.0.0"

    ID = [0, 1]
    Token = ""
    AllianceID = [0, 0]
    HasClub = False
    Name = "Brawler"
    Registered = False
    Thumbnail = 0
    Namecolor = 0
    TeamID = [0, 0]
    Region = "CA"
    ContentCreator = ""

    Coins = 0
    Gems = 10000000
    StarPoints = 0
    Trophies = 0
    HighestTrophies = 500
    TrophyRoadTier = 1
    Experience = 0
    Level = 500
    Tokens = 0
    TokensDoubler = 1000
    Bling = 0
    ChromaticCoins = 0
    RecruitTokens = 0
    PowerPoints = 0

    SelectedSkin = 0
    SelectedBrawler = 0
    RandomizerSelectedSkins = []
    OwnedPins = []
    OwnedThumbnails = []
    OwnedSkins = []
    OwnedSprays = []
    SelectedSkins = {
    "0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "",
    "10": "", "11": "", "12": "", "13": "", "14": "", "15": "", "16": "", "17": "", "18": "", "19": "",
    "20": "", "21": "", "22": "", "23": "", "24": "", "25": "", "26": "", "27": "", "28": "", "29": "",
    "30": "", "31": "", "32": "", "33": "", "34": "", "35": "", "36": "", "37": "", "38": "", "39": "",
    "40": "", "41": "", "42": "", "43": "", "44": "", "45": "", "46": "", "47": "", "48": "", "49": "",
    "50": "", "51": "", "52": "", "53": "", "54": "", "55": "", "56": "", "57": "", "58": "", "59": "",
    "60": "", "61": "", "62": "", "63": "", "64": "", "65": "", "66": "", "67": "", "68": "", "69": "",
    "70": "", "71": "", "72": "", "73": "", "74": ""
    }
    OwnedBrawlers = {
        0: {'CardID': 0, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'MasteryPoints': 29000, 'MasteryTier': 0},
    }
    OwnedTitles = []
    OwnedAccessories = []
    
    GatchaItems = {}
    PurchasedOffers = []
    
    Pass32Int = 0
    Pass64Int = 0
    Pass96Int = 0
    
    Pass32IntP = 0
    Pass64IntP = 0
    Pass96IntP = 0
    
    
    BrawlPassActive = False
    
    RoadType = 0
    PassLevel = 0
    PassSeason = 0
    
    RecruitBrawler = 1
    RecruitCost = 160
    RecruitGemsCost = 29
    RecruitBrawlerCard = 4
    
    BattleIcon1 = 0
    BattleIcon2 = 0
    BattleEmote = 0
    Title = 0
    
    BattleIcon1Visible = False
    BattleIcon2Visible = False
    BattleEmoteVisible = False
    TitleVisible = False
    
    FavouriteBrawler = 0
    
    
    Brawlers = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,34,36,37,40,42,43,45,47,48,50,52,58,61,63,64,67,69,71, 73]
    
    DropRarity = None
    DropAmount = 0
    DailyWins = 0
    
    
    SeenNotifications = []
    
    Notifications = [{"Type": 64, "Readed": True,"Timer": 99999, "Text": "Test", "RewardType": 10, "Amount": 1, "Number": 0, "ItemName": "Gems", "Extra": 0, "Brawler": 0, "BrawlerCard": 0, "BrawlerPower": 1, "StarrDrops": False}]
    
    Quests = [{"MissionType": 1, "AchievedGoal": 1, "QuestGoal": 5000, "GameMode": 3, "Brawler": 0, "QuestReward": 1, "Amount": 500, "CurrentLevel": 0, "MaxLevel": 0, "Time": 99999, "NeedsPass": False, "Complete": False, "Number": 0}]
    
    ClaimedLoginRewardIndex = -1
    LoginRewardIndex = 0
    
    DailyFreebieItem = random.choice(daily_freebie_items)
    DailyFreebieItemAmount = random.randint(25, 350)
    DailyFreebieClaimed = False

    Friends = []
    LastOnline = 0


    def __init__(self):
        pass

    def getDataTemplate(self, highid, lowid, token):
        if highid == 0 or lowid == 0:
            self.ID[0] = int(''.join([str(random.randint(0, 9)) for _ in range(1)]))
            self.ID[1] = int(''.join([str(random.randint(0, 9)) for _ in range(8)]))
            self.Token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(40))
        else:
            self.ID[0] = highid
            self.ID[1] = lowid
            self.Token = token

        DBData = {
            'ID': self.ID,
            'Token': self.Token,
            'AllianceID': self.AllianceID,
            'HasClub': self.HasClub,
            'Name': self.Name,
            'Registered': self.Registered,
            'Thumbnail': self.Thumbnail,
            'Namecolor': self.Namecolor,
            'Region': self.Region,
            'ContentCreator': self.ContentCreator,
            'Coins': self.Coins,
            'Gems': self.Gems,
            'StarPoints': self.StarPoints,
            'TeamID': self.TeamID,
            'Trophies': self.Trophies,
            'HighestTrophies': self.HighestTrophies,
            'TrophyRoadTier': self.TrophyRoadTier,
            'Experience': self.Experience,
            'Level': self.Level,
            'Tokens': self.Tokens,
            'TokensDoubler': self.TokensDoubler,
            'SelectedBrawler': self.SelectedBrawler,
            'SelectedSkin': self.SelectedSkin,
            'OwnedPins': self.OwnedPins,
            'OwnedSprays': self.OwnedSprays,
            'SelectedSkins': self.SelectedSkins,
            'OwnedThumbnails': self.OwnedThumbnails,
            'OwnedBrawlers': self.OwnedBrawlers,
            'OwnedSkins': self.OwnedSkins,
            'OwnedTitles': self.OwnedTitles,
            'OwnedAccessories': self.OwnedAccessories,
            'Bling': self.Bling,
            'ChromaticCoins': self.ChromaticCoins,
            'RecruitTokens': self.RecruitTokens,
            'PowerPoints': self.PowerPoints,
            'GatchaItems': self.GatchaItems,
            'PurchasedOffers': self.PurchasedOffers,
            'Pass32Int': self.Pass32Int,
            'Pass64Int': self.Pass64Int,
            'Pass96Int': self.Pass96Int,
            'Pass32IntP': self.Pass32IntP,
            'Pass64IntP': self.Pass64IntP,
            'Pass96IntP': self.Pass96IntP,
            'BrawlPassActive': self.BrawlPassActive,
            'RoadType': self.RoadType,
            'PassLevel': self.PassLevel,
            'PassSeason': self.PassSeason,
            'RecruitBrawler': self.RecruitBrawler,
            'RecruitCost': self.RecruitCost,
            'RecruitGemsCost': self.RecruitGemsCost,
            'RecruitBrawlerCard': self.RecruitBrawlerCard,
            'Brawlers': self.Brawlers,
            'BattleIcon1': self.BattleIcon1,
            'BattleIcon2': self.BattleIcon2,
            'BattleEmote': self.BattleEmote,
            'Title': self.Title,
            'BattleIcon1Visible': self.BattleIcon1Visible,
            'BattleIcon2Visible': self.BattleIcon2Visible,
            'BattleEmoteVisible': self.BattleEmoteVisible,
            'TitleVisible': self.TitleVisible,
            'FavouriteBrawler': self.FavouriteBrawler,
            'DropRarity': self.DropRarity,
            'DropAmount': self.DropAmount,
            'SeenNotifications': self.SeenNotifications,
            'Notifications': self.Notifications,
            'Quests': self.Quests,
            'ClaimedLoginRewardIndex': self.ClaimedLoginRewardIndex,
            'LoginRewardIndex': self.LoginRewardIndex,
            'DailyWins': self.DailyWins,
            'DailyFreebieItem': self.DailyFreebieItem,
            'DailyFreebieItemAmount': self.DailyFreebieItemAmount,
            'DailyFreebieClaimed': self.DailyFreebieClaimed,
            'Friends': self.Friends,
            'LastOnline': self.LastOnline
            
        }
        return DBData

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4))