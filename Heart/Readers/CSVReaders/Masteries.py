import csv

class Masteries:
    def getMasteryVanityReward(BrawlerID):
        print(BrawlerID)
        with open('Heart/Readers/mastery_hero_confs.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            print(csv_reader)
            for row in csv_reader:

                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    if row[0] == f"Mastery{BrawlerID}":
                        VanityData = {"BrawlerID": {BrawlerID},"EmoteID": row[1], "ThumbnailID": row[2], "TitleID": row[3]}
                        print(VanityData)
                        break
                    if row[0] != "":
                        line_count += 1
        return VanityData
        
    def getMasteryReward(LevelID):
        with open('Heart/Readers/mastery_levels.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    if row[0] == f"Mastery{LevelID}":
                        MasteryData = {"LevelID": {LevelID + 2},"RewardAmount": row[1], "RewardName": row[2], "CsvID": row[4], "SkinID": row[5], "BoxID": row[3]}
                        print(MasteryData)
                        break
                    if row[0] != "":
                        line_count += 1
        return MasteryData
    
    