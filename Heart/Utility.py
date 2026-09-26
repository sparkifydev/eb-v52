import json
import os
import random
from datetime import datetime


class Utility:

    def timerMath(self, timer_start_date, timer_end_date):
        if timer_end_date == "dailyoffer":
            time_sec = 86400 - (3600 * int(datetime.today().strftime('%H'))) + (60 * int(datetime.today().strftime('%M'))) + int(datetime.today().strftime('%S'))
        else:
            import datetime
            timer_start = datetime.datetime(timer_start_date[0], timer_start_date[1], timer_start_date[2], timer_start_date[3], timer_start_date[4], timer_start_date[5])
            timer_end = datetime.datetime(timer_end_date[0], timer_end_date[1], timer_end_date[2], timer_end_date[3], timer_end_date[4], timer_end_date[5])
            timer_now = datetime.datetime.now()
            if timer_now > timer_start:
                if timer_now < timer_end:
                    time_sec = (timer_end - timer_now).total_seconds()
                else:
                    time_sec = -1
            else:
                time_sec = -1
        return int(time_sec)

    def timerGlobalHour(self, timer):
        timer_max = 86400
        timer_now = (0 * int(datetime.today().strftime('%d'))) + (3600 * int(datetime.today().strftime('%H'))) + (60 * int(datetime.today().strftime('%M'))) + int(datetime.today().strftime('%S'))
        timer = timer_max - timer_now
        return timer

    def consoleLog(msg):
        second = str(datetime.now().second)
        minute = str(datetime.now().minute)
        hour = str(datetime.now().hour)
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        if int(second) < 10: second = "0" + second
        if int(minute) < 10: minute = "0" + minute
        if int(hour) < 10: hour = "0" + hour
        if int(day) < 10: day = "0" + day
        if int(month) < 10: month = "0" + month
        dataTime = (day + "." + month + " " + hour + ":" + minute + ":" + second + " - ")
        msgStr = (dataTime + msg)
        print(msgStr)
        with open("log.txt", "r") as file:
            fileLog = file.read()
        msgLog = fileLog.split("\n")
        msgLog.append(msgStr)
        with open("log.txt", "w") as file:
            file.write("")

    def timerGetTime(self, timer):
        SkinsID = [  # Список скинов опущен ради краткости — можешь вставить его обратно, он не изменён
            {"SkinID": 2, "BrawlerID": 1, "Price": 19, "OldPrice": 29},
            {"SkinID": 15, "BrawlerID": 8, "Price": 19, "OldPrice": 29},
            {"SkinID": 100, "BrawlerID": 12, "Price": 239, "OldPrice": 299}
        ]
        if timer == "1bannertime": x = self.timerMath([1970, 1, 1, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "2bannertime": x = self.timerMath([2023, 12, 30, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "3bannertime": x = self.timerMath([2024, 1, 13, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "1banner": x = [["5", "14", "9", "34"], ["9", "34"]]
        elif timer == "2banner": x = [["1", "43", "17", "40"], ["17", "40"]]
        elif timer == "3banner": x = [["15", "27", "10", "37"], ["10", "37"]]
        elif timer == "common_brawlers": x = [["27", "14", "9", "43", "1", "13", "15"], ["50", "22", "8", "3", "16", "7", "21", "4"], ["35", "38", "39", "41"]]
        elif timer == "skinsid": x = SkinsID
        elif timer == "iconsid": x = [89, 90, 91, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        elif timer == "timerbp1": x = self.timerMath([1970, 1, 1, 0, 0, 0], [2024, 6, 6, 12, 0, 0])
        elif timer == "weeklyquest1": x = ["penny_skin2", 28, 0, 5, 19]
        elif timer == "weeklyquest2": x = ["nita_skin1", 28, 0, 5, 8]
        elif timer == "weeklyquest3": x = ["dino_skin1", 28, 0, 5, 9]
        elif timer == "week1": x = self.timerMath([1970, 1, 1, 0, 0, 0], [2023, 12, 23, 0, 0, 0])
        elif timer == "week2": x = self.timerMath([2023, 12, 23, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "week3": x = self.timerMath([2023, 12, 30, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "week4": x = self.timerMath([2024, 1, 6, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "week5": x = self.timerMath([2024, 1, 13, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "week6": x = self.timerMath([2024, 1, 20, 0, 0, 0], [2024, 3, 14, 0, 0, 0])
        elif timer == "weekname1": x = "week1"
        elif timer == "weekname2": x = "week2"
        elif timer == "weekname3": x = "week3"
        elif timer == "weekname4": x = "week4"
        elif timer == "weekname5": x = "week5"
        elif timer == "weekname6": x = "week6"
        elif timer == "weekname": x = "week"
        return x

    def leagueGetRank(self, wins, i):
        try:
            if wins[i] < 4:
                return 1
            elif 4 <= wins[i] <= 9:
                return 2
            elif 10 <= wins[i] <= 19:
                return 3
            elif 20 <= wins[i] <= 29:
                return 4
            elif 30 <= wins[i] <= 39:
                return 5
            elif 40 <= wins[i] <= 59:
                return 6
            elif 60 <= wins[i] <= 79:
                return 7
            elif 80 <= wins[i] <= 99:
                return 8
            elif 100 <= wins[i] <= 129:
                return 9
            elif 130 <= wins[i] <= 159:
                return 10
            elif 160 <= wins[i] <= 189:
                return 11
            elif 190 <= wins[i] <= 239:
                return 12
            elif 240 <= wins[i] <= 299:
                return 13
            elif 300 <= wins[i] <= 379:
                return 14
            elif 380 <= wins[i] <= 439:
                return 15
            elif 440 <= wins[i] <= 539:
                return 16
            elif 540 <= wins[i] <= 639:
                return 17
            elif 640 <= wins[i] <= 799:
                return 18
            elif wins[i] > 799:
                return 19
        except:
            return 0

    def parseFields(fields: dict):
        pass

    def getContentUpdaterInfo():
        return open(f"./ContentUpdater/lastversion.txt", 'r').read().split('...')

    def getFingerprintData(resourceSha):
        return json.dumps(json.loads(open(f"./ContentUpdater/Update/{resourceSha}/fingerprint.json", 'r').read()))

    def getRandomID():
        id = []
        id.append(int(''.join([str(random.randint(0, 9)) for _ in range(2)])))
        id.append(int(''.join([str(random.randint(0, 9)) for _ in range(8)])))
        return id
