

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
import pydle
####variables
config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}

botName = "none"

youtube = ""

firstRun = "on"
discordInfo = {}
discordRoles = {}
#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""

haltDiscordMSG = 0
haltDeleteMSG = 0 

#config  = {"IRCToDiscordFormatting": "{1} : {2}", "channelName": "serverchat", "discordToIRCFormating": "{0} : {1}", "discordToken": "MzM2MzMzMDg1Mzg3OTE1Mjc2.DE21Bw.VnzklzkKApU2wigbsNGnTVrsNNg", "ircChannel": "#popicraft", "ircNickname": "DiscordBot", "ircPassword": "", "ircPort": "6667", "ircServerIP": "irc.popicraft.net", "pageToken": "", "serverName": "Popicraft Minecraft","Bots": {"Discord": {"Channels":{"serverchat":{"formatting":"{0}{1}", "send": True, "sendTo": {"console": {"type": "Discord", "send": False}}}}}}}






#irc stuff
import pydle

ircClient = 0
discordMSG = []

#irc

customStart = ""

##Youtube api stuff
#youtube stuff imported
import httplib2

import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import time



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

botName = "none"

youtube = ""

firstRun = "off"

#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""

haltDiscordMSG = 0
haltDeleteMSG = 0

mainMsg = []
tempRole = 0
discordMembers = {}
processedCommand = []
processedMSG = []
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
    global config, discordInfo,discordRoles
    await client.send_message(discordInfo[msg["Server"]][msg["ChannelTo"]], msg["msgFormated"]["Discord"]) #sends the message to the channel specified in the beginning
    
async def discordCheckMsg(): #checks for a discord message
    global processedMSG, haltDiscordMSG, haltDeleteMSG, config
    j = 0
    for msg in processedMSG: #this cycles through the array for messages unsent to discord and sends them
        if msg["sent"] == False and msg["sendTo"]["Bot"] == "Discord": 
            #await discordSendMsg(msg) #sends message
            await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            processedMSG[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1
        
        
async def discordCheckCommand(): #checks for a discord message
    global processedCommand, haltDiscordMSG, haltDeleteMSG, config,discord,discordMembers
    j = 0
    for command in processedCommand: #this cycles through the array for messages unsent to discord and sends them
        if command["sent"] == False: 
            if command["Command"] == "setRole":
                await client.add_roles(command["authorData"], discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif command["Command"] == "removeRole":
                print("removing")
                await client.remove_roles(command["authorData"], discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif  command["Command"] == "sendMessage":
                print("placeholder")
            elif command["Command"] == "deleteMessage":
                print("deleting message")
                await client.delete_message(command["args"][0])
            
            
            
                
            #await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            processedCommand[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1

@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    global ircClient, discord,discordRoles,tempRole,discordMembers
    firstRun = "off"
    if firstRun == "off":
        #print(discord.Server)
        #these 2 variables are used to keep track of what channel is thre real channel to use when sending messages to discord
        global config , botName, discordMSG,discordInfo, haltDiscordMSG,haltDeleteMSG
        global channelToUse #this is where we save the channel information (i think its a class)
        global  channelUsed #this is the channel name we are looking for
        #this is just to show what the name of the bot is and the id
        print('Logged in as') ##these things could be changed a little bit here
        print(client.user.name+ "#" + client.user.discriminator)
        botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
        print(client.user.id)
        rolesList = {}
        membersList = {}
        for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
            for members in server.members:
                membersList.update({str(members): members})
            discordMembers.update({str(server.name):membersList})
            print(discordMembers) 
            for roles in server.roles:
                print( "[" + server.name + "]"+ roles.name + ":" + str(roles.position))
                rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
                if roles.name == "Mod":
                    tempRole = roles
            discordRoles.update({str(server.name):rolesList})
            print(discordRoles)
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
    # global mainMsg,discord,tempRole,discordRoles,processedCommand
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
            # print(tempRole)
            # # commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            # # processedCommand.append(commandStats)
            # # await client.add_roles(message.author, discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            # msgStats = {"sentFrom":"Discord","deleted": True,"msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":message.content,"sent":False}
            # mainMsg.append(msgStats)
    
@client.event
async def on_error(event):
    print("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    f = open("error.log","r+")
    f.write("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    f.close()
    
    
@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    global mainMsg,discord,tempRole,discordRoles,processedCommand
    if firstRun == "off":
        if str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            print("{0} : {1}".format(message.author,message.content)) #prints this to the screen
            #await client.send_message(message.channel, 'Hello.')          
            #ircSendMSG(message.author,config["ircChannel"],message.content)
            roleList = {}
            for roles in message.author.roles:
                print(roles.name + ":" + str(roles.position))
                roleList.update({str(roles.name):int(roles.position)})
            print(roleList)
            print(tempRole)
            #commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            #processedCommand.append(commandStats)
            #await client.add_roles(message.author, discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            msgStats = {"sentFrom":"Discord","msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":message.content,"sent":False}
            mainMsg.append(msgStats)

            
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


##this is the event loop for the irc client
class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        for key, val in config["Bot"]["IRC"]["Servers"]["None"]["Channel"].items():
            self.join(key)
        

    def on_join(self, channel, user):
        super().on_join(channel, user)
        
    def on_disconnect(self,expected): #this event detects disconnects
        global config
        #this will stop the irc event loop from running in the event that something goes wrong and the connection fails
        print(expected) #prints a debug of if the client disconnected
        retry =  0 #sets the 
        time.sleep(15) #waits a few seconds till the first retry
        while retry <= 50: #forces a reconnect if something goes wrong
            self._reset_connection_attributes() #resets connection info
            print("retrying connection") 
            self.connect(config["Bot"]["IRC"]["IP"],config["Bot"]["IRC"]["Port"]) #starts the connection
            time.sleep(15) #waits so the client can finish connecting and things can actually be processes
            print(self.connected) #status connected or not
            if self.connected: #if connected to irc server leave this loop and be done.
                retry = 59
            else:
                self.connection.stop() #alternative if it failes and go through the previous method that worked partially.
            retry = retry + 1 #keeps going up till the number or retries is hit

        
    def on_channel_message(self,target,by,message):
        global mainMsg
        #self.connection.stop() #this stops the event loop when the client gives up just need to figure out how to determine that
        super().on_channel_message(target,by,message) 
        print(target + ":" + by +  ":" + message )
        msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": "None","Channel": target, "author": by,"authorData": None,"authorsRole": {"Normal": 0},"msg":message,"sent":False}
        mainMsg.append(msgStats)

class irc():#alot of this code was given to me from a friend then i adapted to more of what i needed
    def __init__(self):
        self.messagepattern = re.compile(r"^:(.{1,50})!")
    
    async def irc_bot(self, loop,host): #this all works, well, except for when both SweetieBot and SweetieBot_ are used. -- prints will be removed once finished, likely.
        #host = config["Bot"]["IRC"]["IP"]
        for sKey, sVal in config["Bot"]["IRC"]["Servers"].items():
            self.writer = {}
            self.reader = {}
            host = sKey
            self.readerBasic, self.writerBasic = await asyncio.open_connection(host,config["Bot"]["IRC"]["Servers"][sKey]["Port"], loop=loop)
            self.reader.update({sKey: self.readerBasic})
            self.writer.update({sKey: self.writerBasic})
            await asyncio.sleep(3)
            if config["Bot"]["IRC"]["Servers"][sKey]["Password"] != "":
                self.writer[sKey].write(b'PASS ' + config["Bot"]["IRC"]["Servers"][sKey]["Password"].encode('utf-8') + b'\r\n')
            
            print('[Twitch] ', 'setting nick')
            
            self.writer[sKey].write(b'NICK ' + config["Bot"]["IRC"]["Servers"][sKey]["Nickname"].encode('utf-8') + b'\r\n')
            print('[Twitch] ', 'setting user')
            self.writer[sKey].write(b'USER ' + config["Bot"]["IRC"]["Servers"][sKey]["Nickname"].encode('utf-8') + b' B hi :' + config["Bot"]["IRC"]["Servers"][sKey]["Nickname"].encode('utf-8') + b'\r\n')
            await asyncio.sleep(3)
            for key, val in config["Bot"]["IRC"]["Servers"][sKey]["Channel"].items():
                print(key)
                self.writer[sKey].write(b'JOIN ' + key.encode('utf-8')+ b'\r\n')
            await asyncio.sleep(3)
            print("sending msg")
            #writer.write(b'JOIN #' + "test".encode('utf-8')+ b'\r\n')
            #writer.write("PRIVMSG #test :mods".encode('utf-8')+ b'\r\n')
            
    async def handleSendMsg(self,loop):
        global processedMSG,config
        #irc msg handler
        print("looping")
        while True:
            j = 0
            #print("lo")
            for msg in processedMSG: #this cycles through the array for messages unsent to irc and sends them
                #print(msg["sendTo"])
                if msg["sent"] == False and msg["sendTo"]["Bot"] == "IRC":
                    #print(msg["msgFormated"])
                    #self.writer.write(b'PRIVMSG #test '+b' :' + msg["msgFormated"].encode("utf-8") + b'\r\n')
                    await self.sendMSG(msg["sendTo"]["Server"],msg["sendTo"]["Channel"],msg["msgFormated"])
                    #sends the message to the irc from whatever
                    processedMSG[j]["sent"] = True#promptly after sets that to the delete code
                j = j + 1
            await asyncio.sleep(1)
            
            
    async def handleMsg(self,loop):
        info_pattern = re.compile(r'00[1234]|37[526]|CAP')
        await asyncio.sleep(1)
        while True:
            for sKey, sVal in config["Bot"]["IRC"]["Servers"].items(): 
                #this should check to see if the host or ip was used and initialized before trying to read from it
                if sKey in self.reader:
                    try:
                        data = (await self.reader[sKey].readuntil(b'\n')).decode("utf-8")
                    except asyncio.streams.IncompleteReadError:
                        break
                    data = data.rstrip()
                    data = data.split()
                    print(data)
                    if data[0].startswith('@'):
                        data.pop(0)
                    if data == []:
                        pass
                    elif data[0] == 'PING':
                        self.writer.write(b'PONG %s\r\n' % data[1].encode("utf-8"))
                    # elif data[0] == ':user1.irc.popicraft.net' or data[0] ==':irc.popicraft.net' or info_pattern.match(data[1]):
                        # print('[Twitch] ', ' '.join(data))
                        # # generally not-as-important info
                    else:
                        print(data)
                        await self._decoded_send(data, loop,sKey)
    
    async def _decoded_send(self, data, loop,host):
        """TODO: remove discord only features..."""
        
        if data[1] == 'PRIVMSG':
            user = data[0].split('!')[0].lstrip(":")
            m = re.search(self.messagepattern, data[0])
            if m:
                message = ' '.join(data[3:]).strip(':').lower().split()
                print(data[2]+ ":" + user +': '+ ''.join(message))
                msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":''.join(message),"sent":False}
                mainMsg.append(msgStats)
                # if message[0] == '!' + config['Twitch']['command']:
                    # link = message[1]
                    # # print('Command seen: ', message, link if self._check_if_osu(link) else 'False')
                    # # if self._check_if_osu(link):
                        # # await Osu_bot.send_osu_link(link)

                # if message[0] == '!shutdownosu':
                    # loop.stop()
        elif data[1] == 'JOIN':
            #temp
            x = 1
        elif data[1] == 'PART':
            #temp
            x = 1
        elif data[1] == 'NOTICE':
            #temp
            x = 1
        elif data[1] == 'RECONNECT':
            print('[Twitch] ', 'Twitch has requested that I reconnect, This is currently unsupported.')
            loop.stop()

        elif data[0] == "ERROR":
            if ' '.join([data[1],data[2]]) == ":Closing link:":
                print("[Twitch] Lost Connection or disconnected: %s" % ' '.join(data[4:]))
                loop.stop()
                
                
    async def sendMSG(self,server,channel, msg):
        #print("sending")
        self.writer[server].write("PRIVMSG {0} :{1}".format(channel,msg).encode("utf-8") + b'\r\n')
        
        

#this starts everything for the irc client 
##possibly could of put all this in a class and been done with it?
def ircStart():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #loop = asyncio.get_event_loop(loop)
    Twitch_boT = irc()
    loop.create_task(Twitch_boT.irc_bot(loop,config["Bot"]["IRC"]["IP"]))
    loop.create_task(Twitch_boT.handleMsg(loop))
    loop.create_task(Twitch_boT.handleSendMsg(loop))
    loop.run_forever()
    loop.close()

def ircCheck():
    global processedMSG,config
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
        # for msg in processedMSG: #this cycles through the array for messages unsent to irc and sends them
            # #print(msg["sendTo"])
            # if msg["sent"] == False and msg["sendTo"]["Bot"] == "IRC":
                # ircClient.message(msg["sendTo"]["Channel"],msg["msgFormated"])#sends the message to the irc from whatever
                # processedMSG[j]["sent"] = True#promptly after sets that to the delete code
            # j = j + 1
        
#youtube
        
botName = "none"

botUserID = "empty"

youtube = ""

firstRun = "off"

#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Retrieve a list of the liveStream resources associated with the currently
# authenticated user's channel.

def getLiveId(youtube): #this gets the live chat id
    global liveChatId,botUserID #pulls in the bots livechatid and botuserid for further saving and modifying
  
    list_streams_request = youtube.liveBroadcasts().list( #checks for the live chat id through this
        part="snippet", #this is what we look through to get the live chat id
        broadcastStatus="all", #we need both of these to get the live chat id
        broadcastType="all"
    ).execute() #executes it so its not just some object
    liveChatId = list_streams_request["items"][0]["snippet"]["liveChatId"]#sifts through the output to get the live chat id and saves it
    botUserID = list_streams_request["items"][1]["snippet"]["channelId"] #saves the bots channel user id that we will use as a identifier
    print("liveID {0}".format(liveChatId)) #print the live chat id
    #print("BotID" + str(botUserID))
  
 
  
def listChat():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global config
    global youtube
    global mainMsg
    
    list_chatmessages = youtube.liveChatMessages().list( #lists the chat messages
        part="id,snippet,authorDetails", #gets the author details needed and the snippet all of which giving me the message and username
        liveChatId=liveChatId,
        maxResults=500,
        pageToken=config["Bot"]["Youtube"]["pageToken"] #gives the previous token so it loads a new section of the chat
    ).execute() #executes it so its not just some object

    config["Bot"]["Youtube"]["pageToken"] = list_chatmessages["nextPageToken"] #page token for next use
    
    msgCheckRegex = re.compile(r'(:)') #setup for if we happen to need this it should never change either way
    
    for temp in list_chatmessages["items"]: #goes through all the stuff in the list messages list
        message = temp["snippet"]["displayMessage"] #gets the display message
        username = temp["authorDetails"]["displayName"] #gets the users name
        userID = temp["authorDetails"]["channelId"]
        if message != "" and username != "": #this makes sure that the message and username slot arent empty before putting this to the discord chat        
            print(temp)
            fileSave("youtubeMsgJson.json", temp)
            print(userID)
            print(botUserID)
            if userID != botUserID:
                print("{0} {1}".format(username,message))
                msgStats = {"sentFrom":"Youtube","Bot":"Youtube","Server": None,"Channel": config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorRole":None,"msg":message,"sent":False}
                mainMsg.append(msgStats)
            elif userID == botUserID: #if the userId is the bots then check the message to see if the bot sent it.
                try:
                    msgCheckComplete = msgCheckRegex.search(message) #checks the message against the previously created regex for ":"
                    if msgCheckComplete.group(1) != ":": #if its this then go and send the message as normal
                        print("{0} {1}".format(username,message))
                        msgStats = {"sentFrom":"Youtube","msgData": None,"Bot":"Youtube","Server": "None","Channel": config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorRole": youtubeRoles(temp["authorDetails"]),"msg":message,"sent":False}
                        mainMsg.append(msgStats)
                except AttributeError as error:
                    print("{0} {1}".format(username,message))
                    msgStats = {"sentFrom":"Youtube","msgData": None,"Bot":"Youtube","Server": "None","Channel": config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorsRole": youtubeRoles(temp["authorDetails"]),"msg":message,"sent":False}
                    mainMsg.append(msgStats)


def youtubeRoles(authorDetails):
    roles = {}
    if authorDetails["isChatModerator"] == True:
        roles.update({"Mod":2})
    if authorDetails["isChatOwner"] == True:
        roles.update({"Owner":3})
    if authorDetails["isChatSponsor"] == True:
        roles.update({"Sponsor":1})
    roles.update({"Normal": 0})
    print("roles {0}".format(roles))
    return roles 
    
def listLiveStreams():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global config
    global youtube
    global mainMsg            
    x = list_streams_request = youtube.liveStreams().list(
        part="id,snippet",
        mine=True,
        maxResults=50
    ).execute()
    fileSave("youtubeliveStreamsJson.json", x)
    
    
def listLiveBroadcasts():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global config
    global youtube
    global mainMsg            
    x = youtube.liveBroadcasts().list(
    broadcastStatus="all",
    part="id,snippet",
    maxResults=50
  ).execute()
    fileSave("youtubeliveBroadcastsJson.json", x)    

    

    
def sendLiveChat(msg): #sends messages to youtube live chat
    list_chatmessages_inset = youtube.liveChatMessages().insert(
        part = "snippet",
        body = dict (
            snippet = dict(
                liveChatId = liveChatId,
                type = "textMessageEvent",
                textMessageDetails = dict(
                    messageText = msg
                )
            )
        )
    )  
    list_chatmessages_inset.execute()
    #print(list_chatmessages_inset.execute()) #debug for sending live chat messages
  


if __name__ == "__main__":
    args = argparser.parse_args()
        
    youtube = get_authenticated_service(args) #authenticates the api and saves it to youtube
    getLiveId(youtube)        
    
    
def youtubeChatControl():
    global processedMSG
    while True:    
        listChat()
        listLiveStreams()
        listLiveBroadcasts()
        j = 0
        for msg in processedMSG: #this cycles through the array for messages unsent to irc and sends them
            if msg["sent"] == False and msg["sendTo"]["Bot"] == "Youtube":
                sendLiveChat(msg["msgFormated"])#sends the message to the irc from whatever
                processedMSG[j]["sent"] = True
            j = j + 1
        time.sleep(2) 

class twitchBot():
    
    
    
    def getChannelID(self):
        from urllib.parse import urlencode
        from requests import Session
        from requests.adapters import HTTPAdapter
        from requests.exceptions import HTTPError, InvalidURL, ConnectionError
        import json
        
        clientId=config["Twitch"]["clientId"]  #Register a Twitch Developer application and put its client ID here
        accessToken=config["Twitch"]["accessToken"] #Generate an OAuth token with channel_subscriptions scope and insert your token here
         
        channelName= config["Twitch"]["channelName"]  #Put your channel name here
        session=Session()
        channelId=""
         
         
        channelIdUrl="https://api.twitch.tv/kraken/users?login="+channelName
         
        retryAdapter = HTTPAdapter(max_retries=2)
        session.mount('https://',retryAdapter)
        session.mount('http://',retryAdapter)
        #Find the Channel ID
        response = session.get(channelIdUrl, headers={
        'Client-ID': clientId,
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Content-Type': 'application/json'
        })
        try:
            result = json.loads(response.text)
        except:
            result = None
        print(result)
        if (result):
            channelId = result["users"][0]["_id"]
         
        print(channelId)
        return clientId, accessToken, channelId
        #self.setTitle(channelId,clientId,accessToken)
        #self.setGame(channelId,clientId,accessToken)
        
    def setTitle(self,title):
        #initiate the requests library
        from urllib.parse import urlencode
        from requests import Session
        from requests.adapters import HTTPAdapter
        from requests.exceptions import HTTPError, InvalidURL, ConnectionError
        import json
        
        session=Session()
        #channelId=""
         
        clientId, accessToken, channelId =  self.getChannelID()
        
         
        retryAdapter = HTTPAdapter(max_retries=2)
        session.mount('https://',retryAdapter)
        session.mount('http://',retryAdapter)
        #Find the Channel ID
        result = None
        response = None
        apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId
         
        data = {"channel": {"status": title}}
        print(json.dumps(data,sort_keys=True,indent=4))
        #Do the API push data
        response = session.put(apiRequestUrl, headers={
        'Client-ID': clientId,
        'Authorization': 'OAuth '+accessToken,
        "Accept": "application/vnd.twitchtv.v5+json",
        'Content-Type': 'application/json'
        }, data=json.dumps(data,sort_keys=True,indent=4))
        try:
            result = json.loads(response.text)
        except:
            result = None
        print(result) #prints it out
        
        
    def setGame(self,game):
        from urllib.parse import urlencode
        from requests import Session
        from requests.adapters import HTTPAdapter
        from requests.exceptions import HTTPError, InvalidURL, ConnectionError
        import json
        
        session=Session()
        #channelId=""
         
        clientId, accessToken, channelId =  self.getChannelID() 
         
        retryAdapter = HTTPAdapter(max_retries=2)
        session.mount('https://',retryAdapter)
        session.mount('http://',retryAdapter)
        #Find the Channel ID
        result = None
        response = None
         
        apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId
        
        data = {"channel": {"status": game }}
        print(data)
        #Do the API Lookup
        response = session.put(apiRequestUrl, headers={
        'Client-ID': clientId,
        'Authorization': 'OAuth '+accessToken,
        "Accept": "application/vnd.twitchtv.v5+json",
        'Content-Type': 'application/json'
        }, data=json.dumps(data,sort_keys=True,indent=4))
        try:
            result = json.loads(response.text)
        except:
            result = None
        print(result)
    
    def getViewerCount(self):
        from urllib.parse import urlencode
        from requests import Session
        from requests.adapters import HTTPAdapter
        from requests.exceptions import HTTPError, InvalidURL, ConnectionError
        import json
        
        session=Session()
        #channelId=""
         
        clientId, accessToken, channelId =  self.getChannelID() 
         
        retryAdapter = HTTPAdapter(max_retries=2)
        session.mount('https://',retryAdapter)
        session.mount('http://',retryAdapter)
        #Find the Channel ID
        result = None
        response = None
         
        apiRequestUrl="https://api.twitch.tv/kraken/streams/"+channelId
        
        #Do the API Lookup
        response = session.get(apiRequestUrl, headers={
        'Client-ID': clientId,
        'Authorization': 'OAuth '+accessToken,
        "Accept": "application/vnd.twitchtv.v5+json",
        'Content-Type': 'application/json'
        })
        try:
            result = json.loads(response.text)
        except:
            result = None
        if result["stream"] != None:
            return result["stream"]["viewers"]
        else:
            return None
    
    
    
    

        
class mainBot():
    global config , discord
    def main(self):
        print("bot loaded")
        cycle = 0
        #time.sleep(20)
        while True:
            self.checkMSG()
            self.authorMuteTimeCheck()
            if cycle == 120: 
                fileSave("config-test.json",config)
                cycle = 0
            cycle = cycle + 1
            time.sleep(0.2)
            
    ##remember was working on making all the msg code the same
    def checkMSG(self):
        global processedMSG,mainMsg,processedCommand
        j = 0
        for msg in mainMsg: #this cycles through the array for messages unsent to discord and sends them
            if msg["sent"] == False:
                #print(str(msg["authorData"]))
                #try: #this is here to ensure the thread doesnt crash from looking for something that doesnt exist
                if self.blacklistWorkCheck(msg,j) == False and self.commandCheck(msg,j) == False and self.authorMute(msg) == False:
                    #deleted code check
                    try:
                        if msg["deleted"] == True:
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot": msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": "[Deleted] {1} : {2}".format(msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"])),"sent": False}
                            processedMSG.append(msgStats)
                    except KeyError as error:
                        print("not deleted")
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)

                    #all channels catch portion
                    try:
                        #"*" stands for all channels
                        for key, val in config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"]["*"]["sendTo"].items(): #cycles to figure out which channels to send the message to
                            if val["Enabled"] == True and config["Bot"][val["Site"]]["Enabled"] == True and config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Enabled"] == True:#this code checks to see if the message should be disabled and not sent onward
                                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":val["Site"], "Server": val["Server"], "Channel": val["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["Formatting"].format(msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"])),"sent": False}
                                processedMSG.append(msgStats)
                    except KeyError as error:
                        x = 1
                    try:#this is here to ensure the thread doesnt crash from looking for something that doesnt exist
                        for key, val in config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"][msg["Channel"]]["sendTo"].items(): #cycles to figure out which channels to send the message to
                            if val["Enabled"] == True and config["Bot"][val["Site"]]["Enabled"] == True and config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"][msg["Channel"]]["Enabled"] == True and config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Enabled"] == True:#this code checks to see if the message should be disabled and not sent onward
                                print(msg["Bot"])
                                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":val["Site"], "Server": val["Server"], "Channel": val["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["Formatting"].format(msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"])),"sent": False}
                                processedMSG.append(msgStats)
                    except KeyError as error:
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
                mainMsg[j]["sent"] = True
            j = j +1
            
    def authorMuteTimeCheck(self): #this checks to see if the mute time has been up for all the muted users
        for val, key in config["userMuteList"].copy().items(): #copys items to prevent it from editing a dictionary in use
            #print("{0} : {1}".format(val,key))
            
            if key["time"] == "timer":
                #gets the time checked
                config["userMuteList"][val]["timeChecked"]["second"] = int(time.strftime("%S", time.gmtime()))
                config["userMuteList"][val]["timeChecked"]["minute"] = int(time.strftime("%M", time.gmtime()))
                config["userMuteList"][val]["timeChecked"]["hour"] = int(time.strftime("%H", time.gmtime()))
                config["userMuteList"][val]["timeChecked"]["day"] = int(time.strftime("%d", time.gmtime()))
                
                #calculating the time elapsed
                config["userMuteList"][val]["timeElaplsed"]["second"] = config["userMuteList"][val]["timeChecked"]["second"] - int(config["userMuteList"][val]["timeStarted"]["second"])
                config["userMuteList"][val]["timeElaplsed"]["minute"] = config["userMuteList"][val]["timeChecked"]["minute"] - int(config["userMuteList"][val]["timeStarted"]["minute"])
                config["userMuteList"][val]["timeElaplsed"]["hour"] = config["userMuteList"][val]["timeChecked"]["hour"]- int(config["userMuteList"][val]["timeStarted"]["hour"])
                config["userMuteList"][val]["timeElaplsed"]["day"] = config["userMuteList"][val]["timeChecked"]["day"] - int(config["userMuteList"][val]["timeStarted"]["day"])
                
                #converts everything to seconds
                hour = (config["userMuteList"][val]["timeElaplsed"]["day"] * 24) + config["userMuteList"][val]["timeElaplsed"]["hour"]
                minute = (hour * 60) + config["userMuteList"][val]["timeElaplsed"]["minute"]
                second = (minute * 60) + config["userMuteList"][val]["timeElaplsed"]["second"]
                
                # calculates the time muted for to seconds
                timeMutedFor = int(key["timeMutedFor"]["minute"]) * 60
                #debug displaying
                print(second - timeMutedFor)
                print(" ")
                
                # removes user from the mute list when done
                if second >= timeMutedFor:
                    config["userMuteList"].pop(val)
                    

    def authorMute(self,msg): #deletes the message when people mute others
        mute = False
        #cycles through mute list
        for val, key in config["userMuteList"].items():
            #checks if the users name is muted
            if str(msg["authorData"]) == val:
                print("muted") 
                #deletes the message
                commandStats = {"sentFrom":msg["sentFrom"],"Command":"deleteMessage","args": [msg["msgData"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False} 
                processedCommand.append(commandStats)
                mute = True
        print(mute)
        return mute #returns back if it was muted or not
    
    def botNameReformat(self,botName):
        if botName == "Discord":
            return "D"
        elif botName == "IRC":
            return "I"
        elif botName == "Youtube":
            return "Y"

    def blacklistWorkCheck(self,msg,j):
        found = False
        for val in config["wordBlacklist"]:#this part cycles through the actual blacklist
            for split in msg["msg"].split(): #this part cycles through every word in the message
                if split == val and found == False:#this is the check to see if the word matchs the blacklisted one and checks to see if it has already found one for said word
                    commandStats = {"sentFrom":msg["sentFrom"],"Command":"deleteMessage","args": [msg["msgData"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False} #sends delete command
                    processedCommand.append(commandStats)
                    found = True #sets to true if found one blacklisted word
                    print("blacklisted")
                    mainMsg[j]["sent"] = True #sets the message to true so it doesnt get cyclee through again
                    return True
        return False
                    

    def commandCheck(self,msg,j):
        global discordRoles
        realCommand = False
        commandStats = ""
        msgStats = ""
        if msg["msg"].startswith("!") == True and msg["sent"] == False:
            
            tempMsg = msg["msg"].split()
            print("MSG Type {0} {1} {2}".format(type(msg["msg"]),msg["msg"],tempMsg))
            print(config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Commands"])
            roleNum = 0
            for key,val in msg["authorsRole"].items():
                if val > roleNum:
                    roleNum = val
            print(tempMsg)
            try:
                print("before commands")
                for val in config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Commands"][tempMsg[0]]: #loops through the commands
                    print("in Commands")
                    if val["commandType"] == "setRole": #sets a role to the user
                        if  discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                            print("passed the right command and the correct role")
                            commandStats = {"sentFrom":msg["sentFrom"],"Command":"setRole","args": [val["rankToBe"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                    elif val["commandType"] == "removeRole": #removes a role from the user
                        if discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                            print("passed the right command and the correct role")
                            commandStats = {"sentFrom":msg["sentFrom"],"Command":"removeRole","args": [val["rankToBe"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                    elif val["commandType"] == "sendMessage": #sends a message to discord in the channel it was set to
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                    elif val["commandType"] == "setFile" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                        print("placeholder")
                    elif val["commandType"] == "incrementFile" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #increments a file by blank
                        f = open(val["file"], 'r')#opens file
                        file = []
                        print("incrementFile")
                        for line in f: #pulls the file line by line into a array
                            file.append(line)
                        incrementBy = val["incrementBy"].format(int(file[val["lineToIncrement"]])).split() #splits the formatted string
                        if incrementBy[1] == "+" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #checks to see which operation needs to be  done and applys it
                            x = int(incrementBy[0]) + int(incrementBy[2])
                        elif incrementBy[1] == "-":
                            x = int(incrementBy[0]) - int(incrementBy[2])
                        elif incrementBy[1] == "*":
                            x = int(incrementBy[0]) * int(incrementBy[2])
                        elif incrementBy[1] == "/":
                            x = int(incrementBy[0]) / int(incrementBy[2])
                        elif incrementBy[1] == "//":
                            x = int(incrementBy[0]) // int(incrementBy[2])
                        elif incrementBy[1] == "**":
                            x = int(incrementBy[0]) ** int(incrementBy[2])
                        print(x)
            
                        file[val["lineToIncrement"]] = str(x) #converts it back to string and saves it to the array on said line
                        test=""
                        for x in file: #puts it back into the file
                            test = test + x
                        f.close() #closes file
                        f = open(val["file"], 'w') #writes it back to file                        
                        f.write(test)
                    elif val["commandType"] == "readFile" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #reads a file and sends it to the service
                        f = open(val["file"], 'r')#opens file
                        print("readFile")
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(f.read()),"sent": False}
                    elif val["commandType"] == "relayCommand": #will relay a command from said service (IRC,Youtube or discord)
                        print("placeholder")
                    elif val["commandType"] == "twitchSetGame" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        game = msg["msg"][len(tempMsg[0])+1:]
                        twitchBot().setGame(game)
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "twitchSetTitle" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        title = msg["msg"][len(tempMsg[0])+1:]
                        twitchBot().setGame(title)
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "twitchGetViewers" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        viewers = twitchBot().getViewerCount()
                        print("twitch viewers: " + str(viewers))
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],viewers),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "userMute" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        #determining if a time was set for the mute length
                        try:
                            #gets time to set the start time of the mute to later be stored
                            startSecond = int(time.strftime("%S", time.gmtime()))
                            startMinute = int(time.strftime("%M", time.gmtime()))
                            startHour = int(time.strftime("%H", time.gmtime()))
                            startDay = int(time.strftime("%d", time.gmtime()))
                            #clears the lists of info needed
                            muteAddtimeStarted = {"second":startSecond,"minute":startMinute,"hour": startHour, "day":startDay}
                            mutedFor = {"minute": tempMsg[2]}
                            muteAdd = {"time": "timer", "timeStarted": muteAddtimeStarted,"timeChecked": muteAddtimeStarted,"timeMutedFor": mutedFor,"timeElaplsed": muteAddtimeStarted}
                            #print(muteAdd)
                            config["userMuteList"].update({tempMsg[1]:muteAdd})
                            fileSave("config-test.json",config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1],tempMsg[2]),"sent": False}
                        except IndexError as error: #if no mute length then the mute is permenant
                            toAdd = {tempMsg[1]: {"time": "permanent"}}
                            config["userMuteList"].update(toAdd)
                            fileSave("config-test.json",config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse1"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                    elif val["commandType"] == "userUnmute" and discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        # !unmute (username)
                        try:
                            print("unmuted")
                            config["userMuteList"].pop(tempMsg[1])
                            #print message
                            fileSave("config-test.json",config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                        except IndexError as error:
                            print("user not valid")
                            fileSave("config-test.json",config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse1"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                    print("done command check")
                    if commandStats != "":
                        processedCommand.append(commandStats)
                        commandStats = ""
                        return True
                    if msgStats != "":
                        processedMSG.append(msgStats)
                        msgStats = ""
                        return True
                            
            except KeyError as error:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
            
            if tempMsg[0] == "!temp" and discordRoles[msg["Server"]]["Mod"]["Number"] <= roleNum:
                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": "Hi user","sent": False}
                commandStats = {"sentFrom":msg["sentFrom"],"Command":"setRole","args": ["Mod"],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                processedCommand.append(commandStats)
                realCommand = True
           

            if realCommand == True:
                mainMsg[j]["sent"] = True

            
            if commandStats != "":
                processedCommand.append(commandStats)
               
            if msgStats != "":
                processedMSG.append(msgStats)
        print("none")
        return False


        
#this starts everything for the irc client 
##main loop for the code


#deleteThread = threading.Thread(target=deleteIrcToDiscordMsgThread) #this is broken and needs rewriting
#deleteThread.start()

#mainBot().main()
print("test")
chatControlThread = threading.Thread(target=mainBot().main)
chatControlThread.start()

ircCheckThread = threading.Thread(target=ircCheck)#starts my irc check thread which should print false if the irc thread dies.
if config["Bot"]["IRC"]["Enabled"] == True:
    ircCheckThread.start()
    print("IRC Loaded")
else:
    print("IRC not loaded")

# youtubeChatThread = threading.Thread(target=youtubeChatControl)#starts my youtube chat thread
# if config["Bot"]["Youtube"]["Enabled"] == True:
    # youtubeChatThread.start()
    # print("Youtube Loaded")
# else:
    # print("Youtube not loaded")

discordThread = threading.Thread(target=client.run(config["Bot"]["Discord"]["Token"]))#creates the thread for the discord bot
if config["Bot"]["Discord"]["Enabled"] == True:
    print("Discord Loaded")
    discordThread.start()
else:
    print("Discord not loaded")
    
    
# twitchBot().getViewerCount()
# print("ye")


