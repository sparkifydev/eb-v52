import csv


class PlayerThumbnails:
    def getThumbnailsCount(self):
        with open('Heart/Readers/player_thumbnails.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] != "":
                    line_count += 1
            return line_count - 3
        
    def getCostThumbnailsByID(id):
        with open('Heart/Readers/player_thumbnails.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                if line_count == 0 or line_count == 1:
                    line_count += 1
                else:
                    if line_count - 2 == id:
                        SkinCost = {"Bling": row[12], "Diamonds": row[13]}
                        break
                    if row[0] != "":
                        line_count += 1
        return SkinCost