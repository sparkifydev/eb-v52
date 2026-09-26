import json

class CardFetcher:
	def fetchBrawlerCard(brawler):
		CardID = {"CardID": 0}
		CardsData = json.loads(open("Classes/Readers/JSONReaders/Cards.json", 'r').read())
		for x in CardsData:
			if brawler == x["Brawler"]:
				CardID["CardID"] = x["UnlockCard"]
		return CardID
		
		