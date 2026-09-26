import json

class JSONHandler:
    ShopData = json.loads(open("JSON/Shop/Shop.json", 'r').read())
    RareDropsData = json.loads(open("JSON/DropsData/RareDropsData.json", 'r').read())
    SuperRareDropsData = json.loads(open("JSON/DropsData/SuperRareDropsData.json", 'r').read())
    EpicDropsData = json.loads(open("JSON/DropsData/EpicDropsData.json", 'r').read())
    MythicDropsData = json.loads(open("JSON/DropsData/MythicalDropsData.json", 'r').read())
    LegendaryDropsData = json.loads(open("JSON/DropsData/LegendaryDropsData.json", 'r').read())
    LoginData = json.loads(open("JSON/LoginRewards/LoginRewards.json", 'r').read())

    def Preload():
        JSONHandler.ShopData = json.loads(open("JSON/Shop/Shop.json", 'r').read())