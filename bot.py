import time
import cfg
import socket
import random
from riotwatcher import RiotWatcher


# Connect to twitch chat
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send(("PASS " + cfg.PASS + "\r\n").encode('utf-8'))
s.send(("NICK " + cfg.NICK + "\r\n").encode('utf-8'))
s.send(("JOIN #" + cfg.CHAN + "\r\n").encode('utf-8'))


def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + cfg.CHAN + " :" + message
    s.send((messageTemp + "\r\n").encode('utf-8'))
    print("Sent: " + messageTemp)


# Connect to Riot API
w = RiotWatcher(cfg.RiotAPI,default_region=cfg.playerRegion)
playerName = cfg.playerName
playerRegion = cfg.playerRegion


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
    if chatMessage == "!ping":
        sendMessage(s, "Pong! Im alive!")
        time.sleep(1 / (cfg.RATE))
    elif chatMessage == "!LUL":
        sendMessage(s, "LUL LUL LUL")
        time.sleep(1 / (cfg.RATE))
    elif chatMessage == "!quit":
        quit()
    elif "!espam" in chatMessage:
        spaceloc = []
        spcc = 0
        for spc in chatMessage:
            if spc == " ":
                spaceloc.append(spcc)
                spcc += 1
            else:
                spcc += 1
        toCopyEmote = chatMessage[(spaceloc[0] + 1):(spaceloc[1])]
        toCopyMsg = chatMessage[(spaceloc[1] + 1):(len(chatMessage))]
        finalSpam = ""
        for placeSpam in toCopyMsg:
            if placeSpam == " ":
                pass
            else:
                semiSpam = toCopyEmote + " " + placeSpam + " "
                finalSpam = finalSpam + semiSpam
        twitchSpam = finalSpam + " " + toCopyEmote
        sendMessage(s, twitchSpam)
        time.sleep(1 / (cfg.RATE))
    elif chatMessage == "!memebox":
        sendMessage(s, "Kappa Kappa Kappa")
        time.sleep(2)
        sendMessage(s, "Kappa PogChamp Kappa")
        time.sleep(2)
        sendMessage(s, "Kappa Kappa Kappa")
        time.sleep(2)
    elif "!roulette2" in chatMessage:
        ranGun = random.randint(1, 6)
        if ranGun == 6:
            sendMessage(s, "The gun clicks FeelsBadMan :gun: ")
            time.sleep(2)
            sendMessage(s, "BOOM. You're dead FeelsBadMan")
        else:
            sendMessage(s, "The gun clicks FeelsBadMan :gun: ")
            time.sleep(2)
            sendMessage(s, "You survive! FeelsGoodMan")
    elif chatMessage == "!rank":
        summoner = w.get_summoner(name=playerName, region=playerRegion)
        rankedStatsList = w.get_league_entry([summoner["id"]], )[str(summoner["id"])]
        rankedStatsList2 = rankedStatsList[0]
        playerTier = rankedStatsList2["tier"]
        rankedStatsList3 = rankedStatsList2["entries"]
        rankedStatsDic = rankedStatsList3[0]
        playerDivsion = rankedStatsDic["division"]
        playerLP = rankedStatsDic["leaguePoints"]
        sendMessage(s,playerName + " current rank is " + playerTier + " " + playerDivsion + " " + str(playerLP) + " LP")








