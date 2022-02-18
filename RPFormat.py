import sys
from datetime import datetime
import os

wowdir = " "



with open("config.txt", "r+") as configFile:
    lines = configFile.read().splitlines()
    wowdir = lines[0]
    savedir = lines[1]
    if wowdir == "":
        wowdir = input("Please input your world of warcraft directory:")
        if wowdir[-1] == '/':
            wowdir = wowdir + "_retail_/Logs"
        else:
            wowdir = wowdir + "/_retail_/Logs"
        print(wowdir, file=configFile)
    if savedir == "":
        savedir = input("Please input your RP log directory:")
        print(savedir, file=configFile)

def extractData(channel, line):
    if channel == 's':
        date, time, chat = line.split(' ', 2)
        try:
            chat = chat[1:]
            name, says = chat.split(' ', 1)
            says, message = says.split(':', 1)
            if says == 'says':
                return [date, time, name, message]
            return []
        except:
            return []
    if channel == 'w':
        date, time, chat = line.split(' ', 2)
        try:
            chat = chat[1:]
            firstPart, middlePart = chat.split(' ', 1)
            middlePart, lastPart = middlePart.split(':', 1)
            if middlePart == 'whispers':
                return [date, time, firstPart, lastPart]
            elif firstPart == 'To':
                return [date, time, middlePart, lastPart]
            return []
        except:
            return []
    if channel == 'p':
        date, time, chat = line.split(' ', 2)
        try:
            chat = chat[1:]
            channel1, channel2, message = chat.split(':', 2)
            channel = channel1 + ':' + channel2
            channel, name = channel.rsplit(' ' ,1)
            if 'PARTY' in channel:
                if '|' not in name:
                    return ([date, time, name, message])
                return []
            return []
        except:
            return []


wantedRPDateStart = input("On which Day did the RP start? ")
wantedRPDateEnd = input("On which Day did the RP end? ")
wantedRPStart = input("When did the RP start? ")
wantedRPEnd = input("When did the RP end? ")
channel = input("In which channel was the RP? s, p or w? ")
if (channel == 'w'):
    players = input("With whom did you chat? ")
else:
    players = input("Which players were part of this RP (inlucding yourself)? ").split() 


wantedRPDateStart = datetime.strptime(wantedRPDateStart, "%d/%m").date()
wantedRPDateEnd = datetime.strptime(wantedRPDateEnd, "%d/%m").date()
wantedRPStart = datetime.strptime(wantedRPStart, "%X").time()
wantedRPEnd = datetime.strptime(wantedRPEnd, "%X").time()
wantedDateTimeStart = datetime.combine(wantedRPDateStart, wantedRPStart)
wantedDateTimeEnd = datetime.combine(wantedRPDateEnd, wantedRPEnd)

with open(wowdir + "/WoWChatLog.txt") as input:
    emote = ""
    lastMessageAuthor = ""
    path = savedir + "/" + "-".join(players) + "_" + wantedRPDateStart.strftime("%d.%m.%y") + "_" + wantedRPStart.strftime("%X")
    output = open(path, "w+")
    for line in input:
        data = extractData(channel, line)
        if data != []:
            emoteDate = datetime.strptime(data[0],"%m/%d").date()
            emoteTime = datetime.strptime(data[1].rsplit('.',1)[0],"%X").time()
            emoteDateTime = datetime.combine(emoteDate, emoteTime)
        if data != [] and wantedDateTimeStart < emoteDateTime and wantedDateTimeEnd > emoteDateTime and data[2].split('-')[0] in players:
            if lastMessageAuthor == data[2] or lastMessageAuthor == "":
                emote = emote + data[3]
                lastMessageAuthor = data[2]
            else:
                output.write("\n" + emote)
                emote = data[3]
                lastMessageAuthor = data[2]
    output.write(emote)
    output.close()
