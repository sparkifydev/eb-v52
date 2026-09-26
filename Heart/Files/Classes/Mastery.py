import csv

class Mastery:
    def getBrawlPassLvl(reward, BrawlPassSeason, lvlID):
        with open('Classes/Files/assets/csv_logic/milestones.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    if row[0] == f"Mastery_{reward}":
                        MilestoneData = {"reward": MilestoneID, "BrawlPassSeason": BrawlPassSeason, "lvlID": {lvlID}, "PrimaryLvlUpRewardType": row[9], "PrimaryLvlUpRewardCount": row[10], "PrimaryLvlUpRewardData": row[12]}
                        print(MilestoneData)
                        break
        return MilestoneData