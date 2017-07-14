import time
import cfg
import socket
import random
from riotwatcher import RiotWatcher
from twitch import TwitchClient


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
#Connect to Twitch API
client = TwitchClient(client_id=cfg.TwitchAPI)
channelID = ((client.users.translate_usernames_to_ids(cfg.CHAN))[0])["id"]

#Chatter test system
chattersTest = False
chatterTestPeriod = 600
startTime= 0
deltaTime = 0
chatters = []

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
            sendMessage(s,"Number of active people in chat is " + str(len(chatters)) + ". This is " + str(fractionViewers) + "% of the viewers.")
    if chatMessage == "!ping":
        sendMessage(s, "Pong! Im alive!")
    elif chatMessage == "!LUL":
        sendMessage(s, "LUL LUL LUL")
    elif "!espam" in chatMessage:
        wordSpam = chatMessage.split()[1]
        emoteSpam = chatMessage.split()[2]
        finalSpam = emoteSpam
        for letter in wordSpam:
            finalSpam = finalSpam + " " + letter + " " + emoteSpam
        sendMessage(s,finalSpam)
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
        summoner = w.get_summoner(name=cfg.playerName, region=cfg.playerRegion)
        rankedStatsList = (w.get_league_entry([summoner["id"]], )[str(summoner["id"])])[0]
        sendMessage(s,cfg.playerName + " current rank is " + rankedStatsList["tier"] + " " + ((rankedStatsList["entries"])[0])["division"] + " " + str(((rankedStatsList["entries"])[0])["leaguePoints"]) + " LP")
    elif chatMessage == "!chatters2":
        sendMessage(s,"Running chatter count checks. " + str(chatterTestPeriod) + " second run")
        chattersTest = True
        startTime= time.time()
    elif chatMessage == "!rank1":
        challData = w.get_challenger(region=cfg.playerRegion)["entries"]
        challList = []
        for challCount in challData:
            challList.append(challCount["leaguePoints"])
        challList = sorted(challList,reverse=True)
        summoner = w.get_summoner(name=cfg.playerName, region=cfg.playerRegion)
        rankedStatsList = (w.get_league_entry([summoner["id"]], )[str(summoner["id"])])[0]
        if (((rankedStatsList["entries"])[0])["leaguePoints"]) == challList[0]:
            sendMessage(s,"Yes! " + cfg.playerName + " is Rank 1 with " + str((((rankedStatsList["entries"])[0])["leaguePoints"])) + " LP")
        else:
            sendMessage(s,"No FeelsBadMan")