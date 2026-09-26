import json
import time

from DB.DatabaseHandler import DatabaseHandler
from Heart.Utils.ClientsManager import ClientsManager


def iFriends(player_data):
    db = DatabaseHandler()
    friends = []
    allSockets = ClientsManager.GetAll()
    now = int(time.time())
    for friendRef in player_data["Friends"]:
        state = friendRef["Status"]
        if state != 2 and state != 3 and state != 4:
            continue
        friendEntry = db.getPlayerEntry([0, friendRef["IDLow"]])
        if friendEntry is None:
            continue
        friendData = json.loads(friendEntry[2])
        lastOnline = 0
        if friendData["ID"][1] not in allSockets:
            lastOnline = now - friendData["LastOnline"]
            if lastOnline < 0:
                lastOnline = 0
        friends.append({
            "IDHigh": friendData["ID"][0],
            "IDLow": friendData["ID"][1],
            "Name": friendData["Name"],
            "Trophies": friendData["Trophies"],
            "Thumbnail": friendData["Thumbnail"],
            "NameColor": friendData["Namecolor"],
            "FriendState": state,
            "LastOnline": lastOnline,
        })
    return friends


def sOnline(targetEntry, accountIDHigh, accountIDLow, playerStatus):
    from Heart.Messaging import Messaging
    Messaging.sendMessage(24555, {
        "Socket": targetEntry["Socket"],
        "AccountIDHigh": accountIDHigh,
        "AccountIDLow": accountIDLow,
        "IsOnline": True,
        "Status": playerStatus,
    }, targetEntry["CryptoInit"])


def nOnline(selfID, selfData):
    allSockets = ClientsManager.GetAll()
    selfEntry = allSockets[selfID[1]]
    playerStatus = selfEntry["PlayerStatus"]
    for friendRef in selfData["Friends"]:
        if friendRef["Status"] != 4:
            continue
        friendLow = friendRef["IDLow"]
        if friendLow in allSockets:
            entry = allSockets[friendLow]
            sOnline(entry, selfID[0], selfID[1], playerStatus)


def nFriends(selfID, selfData):
    allSockets = ClientsManager.GetAll()
    currentEntry = allSockets[selfID[1]]
    for friendRef in selfData["Friends"]:
        if friendRef["Status"] != 4:
            continue
        friendLow = friendRef["IDLow"]
        if friendLow in allSockets:
            friendEntry = allSockets[friendLow]
            sOnline(
                currentEntry,
                friendEntry["PlayerIDHigh"],
                friendLow,
                friendEntry["PlayerStatus"],
            )


def nOff(selfID):
    from Heart.Messaging import Messaging
    db = DatabaseHandler()
    allSockets = ClientsManager.GetAll()
    playerEntry = db.getPlayerEntry(selfID)
    if playerEntry is None:
        return
    player_data = json.loads(playerEntry[2])
    db.sLast(selfID)
    for friendRef in player_data["Friends"]:
        if friendRef["Status"] != 4:
            continue
        friendLow = friendRef["IDLow"]
        if friendLow in allSockets:
            entry = allSockets[friendLow]
            Messaging.sendMessage(24555, {
                "Socket": entry["Socket"],
                "AccountIDHigh": selfID[0],
                "AccountIDLow": selfID[1],
                "IsOnline": False,
                "Status": 0,
            }, entry["CryptoInit"])
