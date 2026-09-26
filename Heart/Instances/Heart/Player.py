import json
import random
import string
from Heart.Files.Classes.Cards import Cards
from Heart.Utils.ClientsManager import ClientsManager
from DB.DatabaseHandler import DatabaseHandler

db = DatabaseHandler()
players = db.load_all()
playerscount = len(db.getAll())


class Player:
    ClientVersion = "0.0.0"

    ID = [0, 1]
    AllianceID = [0, 0]
    TeamID = [0, 0]
    Token = ""
    Name = "Brawler"
    Registered = False
    Thumbnail = 0
    Namecolor = 0
    Region = "RU"
    ContentCreator = ""

    Coins = 10000
    CoinsGained = 0
    Gems = 10000
    PowerPoints = 0
    
    GemsGained = 0
    StarPoints = 10000
    StarPointsGained = 0
    Plpoints = 0
    ClubCoins = 0
    Trophies = 10000 
    HighestTrophies = 10000
    TrophiesGained = 0
    TrophyRoadTier = 99999
    Experience = 250
    Level = 500
    Tokens = 200
    TokensGained = 0
    TokensDoubler = 0
    Invitesblckd = 0
    Teamchatmuted = 0
    BrawlPassFreeLevel = []
    BrawlPassLevel = []

    RewardTrackType = 0
    RewardForRank = 0

    BrawlPassSeason = 0
    BrawlPassBuy = 0
    Title = -1
    BattlePin = -1
    BattleIcon1 = -1
    BattleIcon2 = -1
    ProfileBrawler = 0
    threevsthreewins = 0
    FameCredits = 0
    
    PushasedOffers = []
    Titles =[]
    
    delivery_items = {}
    
    IntValueEntry = {'DemoAccount': 0, 'WinStreak': 0, 'EsportButton': 0, 'SocialAge': 1}
    
    Logs = []
    
    banned = False
    
    BPTokens = 0
    
    Notifications = []
    
    BPActivated = False
    
    Challenges = {}

    BrawlersSelectedSkins = {}
    SelectedBrawlers = [0, 1, 8]
    RandomizerSelectedSkins = []
    EnteredCodes = []
    OwnedTitles = []
    OwnedSprays = []
    OwnedPins = []
    OwnedSkins = []
    OwnedThumbnails = []
    OwnedBrawlers = {
        0: {'CardID': 0, 'Skins': [], 'Trophies': 1000, 'HighestTrophies': 1000, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    1: {'CardID': 4, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    2: {'CardID': 8, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    3: {'CardID': 12, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    4: {'CardID': 16, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    5: {'CardID': 20, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    6: {'CardID': 24, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    7: {'CardID': 28, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    8: {'CardID': 32, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    9: {'CardID': 36, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    10: {'CardID': 40, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    11: {'CardID': 44, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    12: {'CardID': 48, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    13: {'CardID': 52, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    14: {'CardID': 56, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    15: {'CardID': 60, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    16: {'CardID': 64, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    17: {'CardID': 68, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    18: {'CardID': 72, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    19: {'CardID': 95, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    20: {'CardID': 100, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    21: {'CardID': 105, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    22: {'CardID': 110, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    23: {'CardID': 115, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    24: {'CardID': 120, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    25: {'CardID': 125, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    26: {'CardID': 130, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    27: {'CardID': 177, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    28: {'CardID': 182, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    29: {'CardID': 188, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    30: {'CardID': 194, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    31: {'CardID': 200, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    32: {'CardID': 206, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    34: {'CardID': 218, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    35: {'CardID': 224, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    36: {'CardID': 230, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    37: {'CardID': 236, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    38: {'CardID': 279, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    39: {'CardID': 296, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    40: {'CardID': 303, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    41: {'CardID': 320, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    42: {'CardID': 327, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    43: {'CardID': 334, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    44: {'CardID': 341, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    45: {'CardID': 358, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    46: {'CardID': 365, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    47: {'CardID': 372, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    48: {'CardID': 379, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    49: {'CardID': 386, 'Skins': [825], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    50: {'CardID': 393, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    51: {'CardID': 410, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    52: {'CardID': 417, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    53: {'CardID': 427, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    54: {'CardID': 434, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    56: {'CardID': 448, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    57: {'CardID': 466, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    58: {'CardID': 474, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    59: {'CardID': 491, 'Skins': [], 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
    60: {'CardID': 499, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        61: {'CardID': 507, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        62: {'CardID': 515, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        63: {'CardID': 523, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        64: {'CardID': 531, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        65: {'CardID': 539, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        66: {'CardID': 547, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        67: {'CardID': 557, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        68: {'CardID': 565, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        69: {'CardID': 573, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        70: {'CardID': 581, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        71: {'CardID': 589, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        72: {'CardID': 597, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        73: {'CardID': 605, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        74: {'CardID': 619, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        75: {'CardID': 633, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        76: {'CardID': 642, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        77: {'CardID': 655, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        78: {'CardID': 663, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0},
        79: {'CardID': 671, 'Trophies': 0, 'HighestTrophies': 0, 'PowerLevel': 1, 'PowerPoints': 0, 'State': 2, 'Mastery': 0, 'ClaimRewardMastery': 0, 'Mastery': 0, 'ClaimRewardMastery': 0}
    }

    def __init__(self):
        pass

    def getDataTemplate(self, highid, lowid, token):
        
        if highid == 0 or lowid == 0:
            self.ID[0] = int(''.join([str(random.randint(1, 9)) for _ in range(1)]))
            self.ID[1] = int(''.join([str(random.randint(1, 9)) for _ in range(8)]))
            self.Token = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(40))
        else:
            self.ID[0] = highid
            self.ID[1] = lowid
            self.Token = token

        DBData = {
            'ID': self.ID,
            'Token': self.Token,
            'Name': self.Name,
            'AllianceID': self.AllianceID,
            'TeamID': self.TeamID,
            'Titles': self.Titles,
            'Registered': self.Registered,
            'Thumbnail': self.Thumbnail,
            'Namecolor': self.Namecolor,
            'Region': self.Region,
            'ContentCreator': self.ContentCreator,
            'Coins': self.Coins,
            'CoinsGained': self.CoinsGained,
            'Gems': self.Gems,
            'GemsGained': self.GemsGained,
            'OwnedSkins': self.OwnedSkins,
            'threevsthreewins': self.threevsthreewins,
            'StarPoints': self.StarPoints,
            'StarPointsGained': self.StarPointsGained,
            'FameCredits': self.FameCredits,
            'ClubCoins': self.ClubCoins,
            'BrawlPassFreeLevel': self.BrawlPassFreeLevel,
            'BrawlPassLevel': self.BrawlPassFreeLevel,
            'RewardTrackType': self.RewardTrackType,
            'RewardForRank': self.RewardForRank,
            'BrawlPassSeason': self.BrawlPassSeason,
            'BrawlPassBuy': self.BrawlPassBuy,
            'Trophies': self.Trophies,
            'IntValueEntry': self.IntValueEntry,
            'HighestTrophies': self.HighestTrophies,
            'TrophiesGained': self.TrophiesGained,
            'TrophyRoadTier': self.TrophyRoadTier,
            'Experience': self.Experience,
            'Level': self.Level,
            'Tokens': self.Tokens,
            'EnteredCodes': self.EnteredCodes,
            'TokensGained': self.TokensGained,
            'TokensDoubler': self.TokensDoubler,
            'PushasedOffers': self.PushasedOffers,
            
                
            'Invitesblckd': self.Invitesblckd,
            'delivery_items': self.delivery_items,
            'Logs': self.Logs,
            'Plpoints': self.Plpoints,
            'ProfileBrawler': self.ProfileBrawler,
            'Teamchatmuted': self.Teamchatmuted,
            'Title': self.Title,
            'BattlePin': self.BattlePin,
            'BattleIcon1': self.BattleIcon1,
            'BattleIcon2': self.BattleIcon2,
            'banned': self.banned,
            'OwnedSprays': self.OwnedSprays,
            'OwnedTitles': self.OwnedTitles,
            'PowerPoints': self.PowerPoints,
            'RandomizerSelectedSkins': self.RandomizerSelectedSkins,
            'BPTokens': self.BPTokens,
            'Notifications': self.Notifications,
            'BPActivated': self.BPActivated,
            'Challenges': self.Challenges,
            'BrawlersSelectedSkins': self.BrawlersSelectedSkins,
            'SelectedBrawlers': self.SelectedBrawlers,
            'OwnedPins': self.OwnedPins,
            'OwnedThumbnails': self.OwnedThumbnails,
            'OwnedBrawlers': self.OwnedBrawlers
        }
        return DBData

    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4))
