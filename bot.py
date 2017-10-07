import time
import cfg
import socket
import random
from riotwatcher import RiotWatcher
from twitch import TwitchClient

print("Starting")

print("Test")

# Connect to Riot API
watcher = RiotWatcher(cfg.RiotAPI)
playerData = watcher.summoner.by_name(cfg.playerRegion, cfg.playerName)
print("Connected to Riot API")

# Connect to Twitch API
client = TwitchClient(client_id=cfg.TwitchAPI, oauth_token=cfg.PASS)
channelID = client.users.translate_usernames_to_ids(cfg.CHAN)[0]["id"]
print("Connected to Twitch API")


def sendmessage(s, message):
    messagetemp = "PRIVMSG #" + cfg.CHAN + " :" + message
    s.send((messagetemp + "\r\n").encode('utf-8'))
    print("Sent: " + messagetemp)


def elo(playersIN):
    currentPlayers = playersIN
    currentPlayersLP = []
    for thePlayer in currentPlayers:
        theirData = (watcher.league.positions_by_summoner(cfg.playerRegion, thePlayer["summonerId"]))[0]
        theirLP = theirData["leaguePoints"]
        if theirData["tier"] == "DIAMOND":
            theirLP = theirLP + 2000
            if theirData["rank"] == "IV":
                theirLP = theirLP + 100
            if theirData["rank"] == "III":
                theirLP = theirLP + 200
            if theirData["rank"] == "II":
                theirLP = theirLP + 300
            if theirData["rank"] == "I":
                theirLP = theirLP + 400
        elif theirData["tier"] == "MASTER" or "CHALLENGER":
            theirLP = theirLP + 2500
        else:
            print("ERROR: " + theirData["playerOrTeamName"] + " is below Diamond!")
        currentPlayersLP.append(theirLP)
    averageLP = int(sum(currentPlayersLP)/len(currentPlayersLP))
    if averageLP > 2500:
        sendmessage(s, "Average player rank in this game: " + str(averageLP - 2500) + " LP")
    elif 2500 >= averageLP > 2400:
        sendmessage(s, "Average player rank in this game: DIAMOND I " + str(averageLP - 2400) + " LP")
    elif 2400 >= averageLP > 2300:
        sendmessage(s, "Average player rank in this game: DIAMOND II " + str(averageLP - 2300) + " LP")
    elif 2300 >= averageLP > 2200:
        sendmessage(s, "Average player rank in this game: DIAMOND III " + str(averageLP - 2200) + " LP")
    elif 2200 >= averageLP > 2100:
        sendmessage(s, "Average player rank in this game: DIAMOND IV " + str(averageLP - 2100) + " LP")
    elif 2100 >= averageLP > 2000:
        sendmessage(s, "Average player rank in this game: DIAMOND V " + str(averageLP - 2000) + " LP")
    elif averageLP <= 2000:
        print("Average LP is lower than Diamond!")

# Connect to twitch chat
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send(("PASS " + cfg.PASS + "\r\n").encode('utf-8'))
s.send(("NICK " + cfg.NICK + "\r\n").encode('utf-8'))
s.send(("JOIN #" + cfg.CHAN + "\r\n").encode('utf-8'))

# Parameters for number of chatters
chattersTest = False
chatterTestPeriod = 600
startTime = 0
deltaTime = 0
chatters = []

# Current time for APi refresh
beginTime = time.time()

while True:
    inc = s.recv(1024).decode("utf-8")
    if inc == "PING :tmi.twitch.tv\r\n":
        s.send(("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
    chatMessage = ""
    chatName = ""
    messagePC = 0
    nameEnd = []
    hashtagEnd = []
    nameLength = len(cfg.CHAN)

    while messagePC<len(inc):
        if inc[messagePC] == "!":
            nameEnd.append(messagePC)
            messagePC += 1
        elif inc[messagePC] == "#":
            hashtagEnd.append(messagePC)
            messagePC += 1
        else:
            messagePC += 1
    if len(nameEnd) > 0 and len(hashtagEnd) > 0:
        chatName = inc[1:nameEnd[0]]
        chatMessage = inc[(hashtagEnd[0]+nameLength+3):(len(inc)-2)]
        print(chatName + ": " + chatMessage)
    if chattersTest is True:
        deltaTime = int("%.0f" % (time.time() - startTime))
        if chatName not in chatters and deltaTime <= chatterTestPeriod:
            print("Added " + chatName)
            chatters.append(chatName)
            print(str(len(chatters)))
        elif deltaTime>chatterTestPeriod:
            chattersTest = False
            viewerNumber = (client.streams.get_stream_by_user(channelID))["viewers"]
            fractionViewers = "%.2f" % ((len(chatters)/viewerNumber) * 100)
            sendmessage(s,"Number of active people in chat is " + str(len(chatters)) + ". This is " + str(fractionViewers) + "% of the viewers.")
    elif chatMessage == "!ping":
        sendmessage(s, "Pong! Im alive!")
    elif chatMessage == "!LuL":
        sendmessage(s, "LuL LuL LuL")
    elif "!espam" in chatMessage:
        wordSpam = chatMessage.split()[1]
        emoteSpam = chatMessage.split()[2]
        finalSpam = emoteSpam
        for letter in wordSpam:
            finalSpam = finalSpam + " " + letter + " " + emoteSpam
        sendmessage(s,finalSpam)
    elif chatMessage == "!memebox":
        sendmessage(s, "Kappa Kappa Kappa")
        time.sleep(2)
        sendmessage(s, "Kappa PogChamp Kappa")
        time.sleep(2)
        sendmessage(s, "Kappa Kappa Kappa")
        time.sleep(2)
    elif "!roulette2" in chatMessage:
        ranGun = random.randint(1, 6)
        if ranGun == 6:
            sendmessage(s, "The gun clicks FeelsBadMan :gun: ")
            time.sleep(2)
            sendmessage(s, "BOOM. You're dead FeelsBadMan")
        else: 
            sendmessage(s, "The gun clicks FeelsBadMan :gun: ")
            time.sleep(2)
            sendmessage(s, "You survive! FeelsGoodMan")
    elif chatMessage == "!rank":
        rankedStatsList = (watcher.league.positions_by_summoner(cfg.playerRegion,playerData["id"]))[0]
        sendmessage(s, "@" + chatName + " " + cfg.playerName + " is currently " + rankedStatsList["tier"] + " " + rankedStatsList["rank"] + " " + str(rankedStatsList["leaguePoints"]) + " LP")
    elif chatMessage == "!chatters2":
        sendmessage(s,"Running chatter count checks. " + str(chatterTestPeriod) + " second run")
        chattersTest = True
        startTime= time.time()
    elif chatMessage == "!rank1":
        challData = watcher.league.challenger_by_queue(cfg.playerRegion,cfg.playerQue)["entries"]
        challNamesLP = {}
        for challCount in challData:
            challNamesLP[challCount["playerOrTeamName"]] = challCount["leaguePoints"]
        challNamesLPSorted = sorted(challNamesLP, key=challNamesLP.get, reverse=True)
        playerLP = (watcher.league.positions_by_summoner(cfg.playerRegion,playerData["id"]))[0]["leaguePoints"]
        if cfg.playerName == challNamesLPSorted[0]:
            sendmessage(s,"Yes! " + cfg.playerName + " is Rank 1 with " + str(playerLP) + " LP")
        else:
            sendmessage(s,"No FeelsBadMan " + cfg.playerName + " is currently " + str(challNamesLP[str(challNamesLPSorted[0])] - (playerLP)) + " LP away from Rank 1. Rank 1 is currently " + str(challNamesLPSorted[0]))
    elif chatMessage == "!runes":
        runeSetup = cfg.playerName + "s current rune page is: "
        for player in watcher.spectator.by_summoner(cfg.playerRegion, playerData["id"])["participants"]:
            if player["summonerName"] == cfg.playerName:
                for rune in player["runes"]:
                    for runeNum, runeName in cfg.allRunes.items():
                        if rune["runeId"] == runeNum:
                            runeSetup = runeSetup + " " + str(rune["count"]) + "X " + runeName + ","

        sendmessage(s, runeSetup)
    elif chatMessage == "!teamelo":
        elo(watcher.spectator.by_summoner(cfg.playerRegion, playerData["id"])["participants"])
