import sys
from datetime import datetime


# wowdir = " "

# with open("config.txt", "r+") as configFile:
#     lines =  configFile.readlines()
#     for line in lines:
#         if (line.split(' ', 1)[0]) == "wowdir":
#             rest, wowdir = line.split(' ', 1)
#             print(wowdir)
#     if wowdir == " ":
#         wowdir = input("Please input your world of warcraft directory:")
#     configFile.writelines("wowdir " + wowdir)

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

with open("WoWChatLog.txt") as input:
    emote = ""
    lastMessageAuthor = ""
    for line in input:
        data = extractData(channel, line)
        if data != []:
            emoteDate = datetime.strptime(data[0],"%m/%d").date()
            emoteTime = datetime.strptime(data[1].rsplit('.',1)[0],"%X").time()
        if data != [] and wantedRPDateStart <= emoteDate and wantedRPDateEnd >= emoteDate and emoteTime >= wantedRPStart and emoteTime <= wantedRPEnd and data[2].split('-')[0] in players:
            if lastMessageAuthor == data[2] or lastMessageAuthor == "":
                emote = emote + data[3]
                lastMessageAuthor = data[2]
            else:
                output.write(emote)
                emote = data[3]
                lastMessageAuthor = data[2]
    path = "-".join(players) + "_" + wantedRPDateStart.strftime("%d\%m") + "_" + wantedRPStart.strftime("%X")
    output = open(path, "w+")
    output.write(emote)
    output.close()
#     open(sys.argv[1]) as input:

#     lastWriter = ''
#     lastEmote = ''
#     block = ''
#     for line in input:
#         start = line.find('[')+1
#         end = line.find(']')
#         emoteStart = line.find(': ')
#         if 'To' in line[:emoteStart]:
#             currentWriter = 'self'
#         else:
#             currentWriter = line[start:end]
#         emote = line[emoteStart+2:].rstrip()
#         if lastWriter == currentWriter:
#             block = block+emote
#         else:
#             output.write(block)
#             block = '\n\n' + emote
#         lastWriter = currentWriter
        
    
