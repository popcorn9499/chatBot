#async to sync
from concurrent.futures import ThreadPoolExecutor
from modules import variables
from modules import mainBot
from modules import fileIO
from modules import youtube


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



firstRun = "on"
discordInfo = {}
#variables.discordRoles = {}
#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""

haltDiscordMSG = 0
haltDeleteMSG = 0 

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
from modules.irc import irc
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




##discord portion of the bot
#this will be the main code

client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)


async def discordSendMsg(msg): #this is for sending messages to discord
    global config, discordInfo
    await client.send_message(discordInfo[msg["Server"]][msg["ChannelTo"]], msg["msgFormated"]["Discord"]) #sends the message to the channel specified in the beginning
    
async def discordCheckMsg(): #checks for a discord message
    global haltDiscordMSG, haltDeleteMSG, config
    j = 0
    for msg in variables.processedMSG: #this cycles through the array for messages unsent to discord and sends them
        if msg["sent"] == False and msg["sendTo"]["Bot"] == "Discord": 
            #await discordSendMsg(msg) #sends message
            await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            variables.processedMSG[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1
        
        
async def discordCheckCommand(): #checks for a discord message
    global haltDiscordMSG, haltDeleteMSG, config,discord
    j = 0
    for command in variables.processedCommand: #this cycles through the array for messages unsent to discord and sends them
        if command["sent"] == False: 
            if command["Command"] == "setRole":
                await mainBot.mainBot().addConsoleAsync('Setting role',"Discord","Extra Info")
                await client.add_roles(command["authorData"], variables.discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif command["Command"] == "removeRole":
                await mainBot.mainBot().addConsoleAsync('Removing role',"Discord","Extra Info")
                await client.remove_roles(command["authorData"], variables.discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif  command["Command"] == "sendMessage":
                await mainBot.mainBot().addConsoleAsync('PlaceHolder for Send message',"Discord","Extra Info")
            elif command["Command"] == "deleteMessage":
                await mainBot.mainBot().addConsoleAsync('Deleted message',"Discord"," Extra Info")
                await client.delete_message(command["args"][0])
            
            
            
                
            #await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            variables.processedCommand[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1

@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    global ircClient
    firstRun = "off"
    if firstRun == "off":
        #print(discord.Server)
        #these 2 variables are used to keep track of what channel is thre real channel to use when sending messages to discord
        global config , botName, discordMSG,discordInfo, haltDiscordMSG,haltDeleteMSG
        global channelToUse #this is where we save the channel information (i think its a class)
        global  channelUsed #this is the channel name we are looking for
        #this is just to show what the name of the bot is and the id
        await mainBot.mainBot().addConsoleAsync('Logged in as',"Discord","Info")##these things could be changed a little bit here
        await mainBot.mainBot().addConsoleAsync(client.user.name+ "#" + client.user.discriminator,"Discord","Info")
        botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
        await mainBot.mainBot().addConsoleAsync(client.user.id,"Discord","Info")
        rolesList = {}
        membersList = {}
        for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
            for members in server.members:
                membersList.update({str(members): members})
            variables.discordMembers.update({str(server.name):membersList})
            await mainBot.mainBot().addConsoleAsync(variables.discordMembers,"Discord","Extra Debug")
            for roles in server.roles:
                #print( "[" + server.name + "]"+ roles.name + ":" + str(roles.position))
                rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
                if roles.name == "Mod":
                    variables.tempRole = roles
            variables.discordRoles.update({str(server.name):rolesList})
            await mainBot.mainBot().addConsoleAsync(variables.discordRoles,"Discord","Extra Debug")
            discordInfo.update({str(server): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
            for channel in server.channels:
                disc = {str(channel.name): channel}
                discordInfo[str(server)].update(disc)
        while True:
            if haltDiscordMSG == 0:
                haltDeleteMSG = 1
                await discordCheckMsg()
                await discordCheckCommand()
                await asyncio.sleep(1)
            
    else:
        await getFirstRunInfo()
                
       
#I need to get the person who deleted this message to make this useful            
# @client.event
# async def on_message_delete(message): #waits for the discord message event and pulls it somewhere
    # global variables.mainMsg,discord,variables.tempRole,variables.discordRoles,variables.processedCommand
    # if firstRun == "off":
        # if str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            # print("[Deleted]{0} : {1}".format(message.author,message.content)) #prints this to the screen
            # # await client.send_message(message.channel, 'Hello.')          
            # # ircSendMSG(message.author,config["ircChannel"],message.content)
            # roleList = {}
            # for roles in message.author.roles:
                # print(roles.name + ":" + str(roles.position))
                # roleList.update({str(roles.name):int(roles.position)})
            # print(roleList)
            # print(variables.tempRole)
            # # commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            # # variables.processedCommand.append(commandStats)
            # # await client.add_roles(message.author, variables.discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            # msgStats = {"sentFrom":"Discord","deleted": True,"msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":message.content,"sent":False}
            # variables.mainMsg.append(msgStats)
    
@client.event
async def on_error(event):
    #print("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    f = open("error.log","r+")
    f.write("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    await mainBot.mainBot().addConsoleAsync("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event),"Discord","Debug")
    f.close()
    
    
@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    if firstRun == "off":
        if str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            #print("{0} : {1}".format(message.author,message.content)) #prints this to the screen
            #await client.send_message(message.channel, 'Hello.')          
            #ircSendMSG(message.author,config["ircChannel"],message.content)
            roleList = {}
            for roles in message.author.roles:
                #await mainBot.mainBot().addConsoleAsync(roles.name + ":" + str(roles.position),"Discord","Info") #causes a weird bot:14 spam in console every message
                roleList.update({str(roles.name):int(roles.position)})
            print(roleList)
            print(variables.tempRole)
            #commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            #variables.processedCommand.append(commandStats)
            #await client.add_roles(message.author, variables.discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            msgStats = {"sentFrom":"Discord","msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":message.content,"sent":False}
            variables.mainMsg.append(msgStats)

            
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

        
        

#this starts everything for the irc client 
##possibly could of put all this in a class and been done with it?
def ircStart():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #loop = asyncio.get_event_loop(loop)
    Twitch_boT = irc()
    loop.create_task(Twitch_boT.irc_bot(loop))
    loop.run_forever()
    loop.close()

def ircCheck():
    global config
    ircThread = threading.Thread(target=ircStart) #creates the thread for the irc client
    ircThread.start() #starts the irc bot
    time.sleep(10)
    # while True:
        # time.sleep(1)
        # state = ircThread.isAlive()
        # if state == False:
            # print("damn it")
            # ircThread = threading.Thread(target=ircStart) #creates the thread for the irc client
            # ircThread.start() #starts the irc bot   
        #irc msg handler
        # j = 0
        # for msg in variables.processedMSG: #this cycles through the array for messages unsent to irc and sends them
            # #print(msg["sendTo"])
            # if msg["sent"] == False and msg["sendTo"]["Bot"] == "IRC":
                # ircClient.message(msg["sendTo"]["Channel"],msg["msgFormated"])#sends the message to the irc from whatever
                # variables.processedMSG[j]["sent"] = True#promptly after sets that to the delete code
            # j = j + 1
        
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

ircCheckThread = threading.Thread(target=ircCheck)#starts my irc check thread which should print false if the irc thread dies.
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

discordThread = threading.Thread(target=client.run(config["Bot"]["Discord"]["Token"]))#creates the thread for the discord bot
if config["Bot"]["Discord"]["Enabled"] == True:
    print("Discord Loaded")
    discordThread.start()
else:
    print("Discord not loaded")
    
    
# twitchBot().getViewerCount()
# print("ye")


