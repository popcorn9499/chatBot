#async to sync
from concurrent.futures import ThreadPoolExecutor
from modules import variables
from modules import mainBot
from modules import fileIO
from modules import youtube
from modules import discordBot

import datetime
#used for the main program
import threading

import json

import sys, os
#discord stuff imported
import discord #gets the discord and asyncio librarys
import asyncio
import time

#irc stuff
####variables
config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}

botName = "none"




#variables.discordRoles = {}
#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""



#config  = {"IRCToDiscordFormatting": "{1} : {2}", "channelName": "serverchat", "discordToIRCFormating": "{0} : {1}", "discordToken": "MzM2MzMzMDg1Mzg3OTE1Mjc2.DE21Bw.VnzklzkKApU2wigbsNGnTVrsNNg", "ircChannel": "#popicraft", "ircNickname": "DiscordBot", "ircPassword": "", "ircPort": "6667", "ircServerIP": "irc.popicraft.net", "pageToken": "", "serverName": "Popicraft Minecraft","Bots": {"Discord": {"Channels":{"serverchat":{"formatting":"{0}{1}", "send": True, "sendTo": {"console": {"type": "Discord", "send": False}}}}}}}






#irc stuff


ircClient = 0
discordMSG = []

#irc

customStart = ""

##Youtube api stuff




##broken
#seems to not like my code in the discordCheckMsg function
##its the part where it sets the value to the delete code.
#this then causes the delete thread to crash trying to find the shift value to go by




##problems
#unsure what will happen in a headless enviroment if the oauth hasnt been set
##if the token and you input a invalid token the first time it will continue to say invalid token for tokens that are even valid



##ideas
#possiblity of use of file io to get the information of the client token for discord and stuff.
#use regex to help format the chat (honestly not needed)


##youtube chat porition
#this will handle getting chat from youtube which will then be pushed to discord

#!/usr/bin/python




####variables
config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}
from modules import irc
botName = "none"


firstRun = "off"

#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""

haltDiscordMSG = 0
haltDeleteMSG = 0


##jadens shift code
#delete code is: 98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98
#delete code is: 98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98
def shift(value, messages):
    if value == 0:
        return messages
    messagesTemp = [] #Assign temp list
    for i in messages: #For every message
        messagesTemp += [i,] #Add to temp list
    messages.clear() #Delete old list
    for i in messagesTemp[value:]: #For all values after last delete code
        messages += [i,] #Take value from temp list and put in new spot
    messagesTemp.clear() #Delete temp list
    return messages

def checkDeleteCode(messages):
    i = 0 #Set i to 0
    #print("{0} : {1}".format(haltDeleteMSG,haltDiscordMSG)) #debug that isnt really nessisary if this code isnt used.
    while(messages[i] == "98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98"): #While value at index is the delete code
        i += 1 #Add 1 to i
    return i #Return value of i when message is not delete code



def deleteIrcToDiscordMsgThread():
    global discordMSG, haltDeleteMSG, haltDiscordMSG
    while True:
        #print(discordMSG)
        #print("{0} : {1}".format(haltDeleteMSG,haltDiscordMSG))
        if haltDeleteMSG == 0:
            haltDiscordMSG = 1
            #shiftValue = checkDeleteCode(discordMSG)
            #discordMSG = shift(shiftValue, discordMSG)
            haltDiscordMSG = 0
        #print(discordMSG)
        time.sleep(4)



            
##file load and save stuff
def fileSave(fileName,config):
    print("Saving")
    f = open(fileName, 'w') #opens the file your saving to with write permissions
    f.write(json.dumps(config,sort_keys=True, indent=4 ) + "\n") #writes the string to a file
    f.close() #closes the file io

def fileLoad(fileName):#loads files
    with open(fileName, 'r') as handle:#loads the json file
        config = json.load(handle) 
    return config



##first run stuff


def getToken(): #gets the token 
    global config
    realToken = "false" #this is just for the while loop
    while realToken == "false":
        config["discordToken"] = input("Discord Token: ") #gets the user input
        try:
            client.run(config["discordToken"]) #atempts to run it and if it fails then execute the next bit of code if not then save it and go on
        except:
            print("Please enter a valid token")
            sys.exit(0) #this is a work around for the bug that causes the code not think the discord token is valid even tho it is after the first time of it being invalid
        else:
            realToken = "true"

async def getFirstRunInfo():
    global config 
    print('Logged in as') ##these things could be changed a little bit here
    print(client.user.name)
    print(client.user.id)
    while config["serverName"] == "":
        for server in client.servers: #this sifts through all the bots servers and gets the channel we want
            print(server.name)
            if input("If this is the server you want type yes if not hit enter: ") == "yes":
                config["serverName"] = server.name
                break    
    while config["channelName"] == "":
        for server in client.servers: #this sifts through all the bots servers and gets the channel we want
            #should probly add a check in for the server in here im guessing
            #print(server.name)
            for channel in server.channels:
                if str(channel.type) == "text":
                    print(channel.name)
                    if input("If this is the channel you want type yes if not hit enter: ") == "yes":
                        config["channelName"] #starts the discord bot= channel.name
                        break
    while config["IRCToDiscordFormatting"] == "": #fills the youtube to discord formating
        config["IRCToDiscordFormatting"] = input("""Please enter the chat formatting for chat coming from irc to go to discord. 
{1} is the placeholder for the username
{2} is the placeholder for the message
Ex. "{0} : {1}: """)
    while config["discordToIRCformating"] == "": #fills the discord to youtube formating
        config["discordToIRCFormating"] = input("""Please enter the chat formatting for chat coming from discord to go to irc. 
{0} is the placeholder for the username
{1} is the placeholder for the message
Ex. "{0} : {1}": """)
    print("Configuration complete")
    fileSave("config-test.json",config) #saves the file
    print("Please run the command normally to run the bot")
    await client.close()
            
if os.path.isfile("config-test.json") == False:#checks if the file exists and if it doesnt then we go to creating it
    print("Config missing. This may mean this is your first time setting this up")
    firstRun = "on"
else:
    config = fileLoad("config-test.json") #if it exists try to load it
if firstRun == "on":
    config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}
    getToken()

        
        


#youtube
        
botName = "none"

botUserID = "empty"


firstRun = "off"

#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""


   
    
    



    
    
    
variables.config = fileIO.fileLoad("config-test.json")    

        


        
#this starts everything for the irc client 
##main loop for the code


#deleteThread = threading.Thread(target=deleteIrcToDiscordMsgThread) #this is broken and needs rewriting
#deleteThread.start()

#mainBot.mainBot().main()
print("test")
chatControlThread = threading.Thread(target=mainBot.mainBot().main)
chatControlThread.start()

ircCheckThread = threading.Thread(target=irc.ircCheck)#starts my irc check thread which should print false if the irc thread dies.
if config["Bot"]["IRC"]["Enabled"] == True:
    ircCheckThread.start()
    print("IRC Loaded")
else:
    print("IRC not loaded")

print(type(youtube))

youtubeChatThread = threading.Thread(target=youtube.youtubeChatControl)#starts my youtube chat thread
if config["Bot"]["Youtube"]["Enabled"] == True:
    youtubeChatThread.start()
    print("Youtube Loaded")
else:
    print("Youtube not loaded")

discordThread = threading.Thread(target=discordBot.client.run(config["Bot"]["Discord"]["Token"]))#creates the thread for the discord bot
if config["Bot"]["Discord"]["Enabled"] == True:
    print("Discord Loaded")
    discordThread.start()
else:
    print("Discord not loaded")
    
    
# twitchBot().getViewerCount()
# print("ye")


