import json
import time
import threading
from Heart.Commands.LogicCommand import LogicCommand
from Heart.Messaging import Messaging
from DB.DatabaseHandler import DatabaseHandler
from Heart.ByteStream import ByteStream
from Heart.Files.Classes.Cards import Cards
from Heart.Files.Classes.Characters import Characters

""" rewards
1 - gems
2 - coins
3 - skin
4 - brawler
5 - пин
6 - иконka
7 - титулы
8 - creдиты """

class LogicViewInboxNotificationCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["NotificationIndex"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        playerData = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])
        playerData["Notifications"] = {
    "Reward": 8,
    "BrawlerID": 1,
    "PowerLevel": 11,
    "Skins": [537],
    "Readed": False,
    "Tokens": 9339 
} #!!! у вас старр дорога упадет если заберёте наградуу
        
        r = playerData["Notifications"]["Reward"]
        u = playerData["Notifications"]["Readed"]
        s = playerData["Notifications"]["Skins"]

        box = {'Type': 100, 'Items': []}
        
        if u:
        	pass

        if r == 3:
            for skin in s:
            	playerData["OwnedSkins"].append(skin)
            	playerData["GatchaItems"] = {'Boxes': []}
            	item = {'Amount': 1, 'DataRef': [29, skin],  'RewardID': 9}
            	box['Items'].append(item)
            	playerData["GatchaItems"]['Boxes'].append(box)
            	self.save(db_instance, playerData, calling_instance, fields, cryptoInit, box)

        elif r == 4:
            brawler_id = playerData["Notifications"]["BrawlerID"]
            bcard = 1488
            if brawler_id == 1: bcard = 4
            elif brawler_id == 2: bcard = 8
            elif brawler_id == 3: bcard = 12
            elif brawler_id == 4: bcard = 16
            elif brawler_id == 5: bcard = 20
            elif brawler_id == 6: bcard = 24
            elif brawler_id == 7: bcard = 28
            elif brawler_id == 8: bcard = 32
            elif brawler_id == 9: bcard = 36
            elif brawler_id == 10: bcard = 40
            elif brawler_id == 11: bcard = 44
            elif brawler_id == 12: bcard = 48
            elif brawler_id == 13: bcard = 52
            elif brawler_id == 14: bcard = 56
            elif brawler_id == 15: bcard = 60
            elif brawler_id == 16: bcard = 64
            elif brawler_id == 17: bcard = 68
            elif brawler_id == 18: bcard = 72
            elif brawler_id == 19: bcard = 95
            elif brawler_id == 20: bcard = 100
            elif brawler_id == 21: bcard = 105
            elif brawler_id == 22: bcard = 110
            elif brawler_id == 23: bcard = 115
            elif brawler_id == 24: bcard = 120
            elif brawler_id == 25: bcard = 125
            elif brawler_id == 26: bcard = 130
            elif brawler_id == 27: bcard = 177
            elif brawler_id == 28: bcard = 182
            elif brawler_id == 29: bcard = 188
            elif brawler_id == 30: bcard = 194
            elif brawler_id == 31: bcard = 200
            elif brawler_id == 32: bcard = 206
            elif brawler_id == 34: bcard = 218
            elif brawler_id == 35: bcard = 224
            elif brawler_id == 36: bcard = 230
            elif brawler_id == 37: bcard = 236
            elif brawler_id == 38: bcard = 279
            elif brawler_id == 39: bcard = 296
            elif brawler_id == 40: bcard = 303
            elif brawler_id == 41: bcard = 320
            elif brawler_id == 42: bcard = 327
            elif brawler_id == 43: bcard = 334
            elif brawler_id == 44: bcard = 341
            elif brawler_id == 45: bcard = 358
            elif brawler_id == 46: bcard = 365
            elif brawler_id == 47: bcard = 372
            elif brawler_id == 48: bcard = 379
            elif brawler_id == 49: bcard = 386
            elif brawler_id == 50: bcard = 393
            elif brawler_id == 51: bcard = 410
            elif brawler_id == 52: bcard = 417
            elif brawler_id == 53: bcard = 427
            elif brawler_id == 54: bcard = 434
            elif brawler_id == 56: bcard = 448
            elif brawler_id == 57: bcard = 466
            elif brawler_id == 58: bcard = 474
            elif brawler_id == 59: bcard = 491
            elif brawler_id == 60: bcard = 499
            elif brawler_id == 61: bcard = 605
            elif brawler_id == 62: bcard = 515
            elif brawler_id == 63: bcard = 523
            elif brawler_id == 64: bcard = 531
            elif brawler_id == 65: bcard = 539
            elif brawler_id == 66: bcard = 547
            elif brawler_id == 67: bcard = 557
            elif brawler_id == 68: bcard = 565
            elif brawler_id == 69: bcard = 573
            elif brawler_id == 70: bcard = 581
            elif brawler_id == 71: bcard = 589
            elif brawler_id == 72: bcard = 597
            elif brawler_id == 73: bcard = 605

            pl = playerData["Notifications"]["PowerLevel"]
            skins = playerData["Notifications"]["Skins"]

            playerData["OwnedBrawlers"][brawler_id] = {
                'CardID': bcard,
                'Skins': [0],
                'Trophies': 0,
                'HighestTrophies': 0,
                'PowerLevel': pl,
                'PowerPoints': 0,
                'State': 2,
                'MasteryPoints': 0,
                'MasteryTier': 0
            }

            playerData["GatchaItems"] = {'Boxes': []}
            item = {'Amount': 1, 'DataRef': [16, brawler_id], 'RewardID': 1}
            box['Items'].append(item)
            playerData["GatchaItems"]['Boxes'].append(box)
            self.save(db_instance, playerData, calling_instance, fields, cryptoInit, box)
            skins = playerData["Notifications"]["Skins"]
            print(skins)


            if skins:
                for skin in skins:
                    print(box)
                    print(skin)
                    box = {'Type': 100, 'Items': []}
                    playerData["OwnedSkins"].append(skin)
                    playerData["GatchaItems"] = {'Boxes': []}
                    item = {'Amount': 1, 'DataRef': [29, skin], 'RewardID': 9}
                    box['Items'].append(item)
                    playerData["GatchaItems"]['Boxes'].append(box)
                    print(box)
                    self.save(db_instance, playerData, calling_instance, fields, cryptoInit, box)
                    
        elif r == 8:
        	amount = playerData["Notifications"]["Tokens"]
        	box = {"Items": []}
        	item = {'Amount': amount, 'DataRef': [16, 0], 'RewardID': 22}
        	playerData["GatchaItems"] = {'Boxes': []}
        	box["Type"] = 100
        	box['Items'].append(item)
        	playerData["GatchaItems"]['Boxes'].append(box)
        	self.save(db_instance, playerData, calling_instance, fields, cryptoInit, box)
        	

        if fields["NotificationIndex"] == 3:
            skin = 52
            box = {'Type': 100, 'Items': []}
            playerData["OwnedSkins"].append(skin)
            playerData["GatchaItems"] = {'Boxes': []}
            item = {'Amount': 1, 'DataRef': [29, skin], 'RewardID': 9}
            box['Items'].append(item)
            playerData["GatchaItems"]['Boxes'].append(box)
            self.save(db_instance, playerData, calling_instance, fields, cryptoInit, box)

    def save(self, db_instance, playerData, calling_instance, fields, cryptoInit, box):
        playerData["Notifications"]["Readed"] = True
        db_instance.updatePlayerData(playerData, calling_instance)
        fields["Socket"] = calling_instance.client
        fields["Command"] = {"ID": 203}
        fields["PlayerID"] = calling_instance.player.ID
        fields["IsBrawlPassReward"] = False
        Messaging.sendMessage(24111, fields, cryptoInit, calling_instance.player)
        box['Items'].clear()
        db_instance.updatePlayerData(playerData, calling_instance)	

    def getCommandType(self):
        return 528
