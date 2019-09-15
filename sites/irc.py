import asyncio
import re

from utils import config
from utils import Object
from utils import logger
from utils import fileIO
from utils import messageFormatter
import sites.emotes
import os
import time
import json

import requests #replace this sometime in the future

##this is the event loop for the irc client
class irc():#alot of this code was given to me from thehiddengamer then i adapted to more of what i needed
    def __init__(self):
        self.messagepattern = re.compile(r"^:(.{1,50})!")
        #variables.config = __main__.variables.config
        self.l = logger.logs("IRC")
        fileIO.checkFolder("config{0}auth{0}".format(os.sep),"auth",self.l)
        fileIO.checkFile("config-example{0}auth{0}irc.json".format(os.sep),"config{0}auth{0}irc.json".format(os.sep),"irc.json",self.l)
        config.c.irc = fileIO.loadConf("config{0}auth{0}irc.json")
        
        self.l.logger.info("Starting")
        self.serviceStarted = {}
        config.events.onMessageSend += self.sendMSG
        self.writer = {}
        self.reader = {}
        self.emoteObjects = [] #this should be just plain emote objects
        self.msgHandlerTasks = {}
        self.hostNicknames = {} #{host: nickname}

    async def irc_bot(self, loop): #this all works, well, except for when both SweetieBot and SweetieBot_ are used. -- prints will be removed once finished, likely.        
        config.events.subscribeEmoteEngine(self,self.emoteObjects)
        for sKey, sVal in config.c.irc["Servers"].items():
            if sVal["Enabled"] == True:
                host = sKey
                print(type(host))
                self.l.logger.info("{0} - Connecting".format(host)) 
                loop.create_task(self.ircConnect(loop,host))
            else:
                await asyncio.sleep(3)
        try:#stops the crash if no irc settings r set
            self.l.logger.info("Connected: " + host)#wtf is this ment for anymore?
        except UnboundLocalError:
            pass
            
    async def ircConnect(self,loop,host):#handles the irc connection
        while True:
            try:
                self.serviceStarted.update({host:False})
                self.readerBasic, self.writerBasic = await asyncio.open_connection(host,config.c.irc["Servers"][host]["Port"], loop=loop)
                self.reader.update({host: self.readerBasic})
                self.writer.update({host: self.writerBasic})
                self.l.logger.debug("{0} - Reader {1} ".format(host,self.reader))
                self.l.logger.debug("{0} - Writer {1} ".format(host, self.writer))
                password=config.c.irc["Servers"][host]["Password"]
                nickname=config.c.irc["Servers"][host]["Nickname"]
                self.hostNicknames.update({host:nickname})
                await self.register(self.writer[host],password,nickname,host)
                self.l.logger.info("{0} - Initiating IRC Reader".format(host))
                self.msgHandlerTasks.update({host: loop.create_task(self.handleMsg(loop,host))})
                self.serviceStarted.update({host:True})
                while not self.msgHandlerTasks[host].done():
                    await asyncio.sleep(5)
            except Exception as e:
                self.l.logger.info(e)
            await asyncio.sleep(10) #retry timeout
        
    async def register(self,writer,password,nickname,host):
        print("WRiter:" + str(writer))
        if password != "":
            writer.write(b'PASS ' + password.encode('utf-8') + b'\r\n')
            self.l.logger.info("{0} - Inputing password ".format(host)) #,"Info")
        self.l.logger.info("{0} - Setting user {1}+ ".format(host,nickname))
        writer.write(b'NICK ' + nickname.encode('utf-8') + b'\r\n')
        self.l.logger.info("{0} - Setting user {1}".format(host, nickname))
        writer.write(b'USER ' + config.c.irc["Servers"][host]["Nickname"].encode('utf-8') + b' B hi :' + config.c.irc["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')

    async def keepAlive(self,loop,host):
        while True:
            try:
                self.writer[host].write("PING {0} ".format(host).encode("utf-8") + b'\r\n')
            except ConnectionResetError:
                self.msgHandlerTasks[host].cancel() #kills the handler task to recreate the entire connection again
                await self.ircConnect(loop,host)
                break
            except asyncio.streams.IncompleteReadError:
                pass
            await asyncio.sleep(60)
            
    async def handleMsg(self,loop,host):
        #info_pattern = re.compile(r'00[1234]|37[526]|CAP')
        while True:
            if host in self.reader:
                try:
                    data = (await self.reader[host].readuntil(b'\n')).decode("utf-8")
                    data = data.rstrip()
                    data = data.split()
                    allData = data[0]
                    self.l.logger.info(' '.join(data) + host) #,"Extra Debug")
                    print(data[0])
                    if data[0].startswith('@'):                      
                        data.pop(0)
                    if data == []:
                        pass
                    elif data[1] == '001': #connect to my channels
                        self.l.logger.info("{0} - Joining channels".format(host))
                        for key, val in config.c.irc["Servers"][host]["Channel"].items():
                            if val["Enabled"] == True:
                                print(key)
                                self.writer[host].write(b'JOIN ' + key.encode('utf-8')+ b'\r\n')
                                self.l.logger.info("{0} - Joining channel {1}".format(host,key))

                        if host == "irc.chat.twitch.tv":
                            self.l.logger.info("Applying for twitch tags")
                            self.writer[host].write(b'CAP REQ :twitch.tv/tags' + b'\r\n')
                        loop.create_task(self.keepAlive(loop,host)) #creates the keep alive task
                    elif data[1] == "433" or data[1] == "436": #handles avoiding nickname conflicts
                        password=config.c.irc["Servers"][host]["Password"]
                        nickname=config.c.irc["Servers"][host]["Nickname"] + "_"
                        self.hostNicknames.update({host:nickname})
                        await self.register(self.writer[host],password,nickname,host)
                    elif data[0] == 'PING':
                        print(data)
                        self.writer[host].write(b'PONG %s\r\n' % data[1].encode("utf-8"))
                    # elif data[0] == ':user1.irc.popicraft.net' or data[0] ==':irc.popicraft.net' or info_pattern.match(data[1]):
                        # print('[Twitch] ', ' '.join(data))
                        #generally not-as-important info
                    else:
                        print(data)
                        await self._decoded_send(data, loop,host,allData)
                except ConnectionResetError:
                    #self.ircConnect(loop,host)
                    break
                except asyncio.streams.IncompleteReadError:
                    pass
                self.l.logger.info("Why am i looping?")
            else:
                print("{0} doesnt exist".format(host))

                
    
    async def processMsg(self,username,message,roleList,server,channel,emojis,badges):
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": "irc","%message%":"message","%roles%":roleList}
        message = Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service="irc",Roles=roleList,emojis=emojis,Badges=badges)
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged="None")
        config.events.onMessage(message=objSendMsg)
    
    async def twitchEmotes(self,message,allData,emojis):
        tempData = allData[1:].split(";") # 1: drops the first bit of information we dont need aka "@"
        for tempPair in tempData:
            tempPair = tempPair.split("=")
            if tempPair[0] == "emotes" and tempPair[1] != '':
                emoteData = tempPair[1].split("/")
                for emotePair in emoteData:
                    emoteID = emotePair.split(":")[0]
                    emoteURL= "http://static-cdn.jtvnw.net/emoticons/v1/{0}/3.0".format(emoteID)
                    #get emote string.
                    emotePos = emotePair.split(":")[1].split(",")[0].split("-")
                    emote=message[int(emotePos[0]):int(emotePos[1])+1]
                    emojis.update({emote: emoteURL})


    async def twitchBadges(self,message,allData,badges):
        roomID = await self.getRoomID(allData)
        tempData = allData[1:].split(";") # 1: drops the first bit of information we dont need aka "@"
        for tempPair in tempData:
            tempPair = tempPair.split("=")
            if tempPair[0] == "badges" and tempPair[1] != '':
                badgeData = tempPair[1].split(",")
                print(badgeData)
                for badgePair in badgeData:
                    badgeName = badgePair.split("/")[0]
                    badgeVersion = badgePair.split("/")[1]
                    #find twitchBadge object
                    for obj in self.emoteObjects:
                        print(type(obj))
                        if (isinstance(obj, sites.emotes.twitchBadges.twitchBadges)):
                            await obj.getBadges(badgeName,badgeVersion,badges,roomID)
                            break
                            
    async def getRoomID(self,allData):
        tempData = allData[1:].split(";") # 1: drops the first bit of information we dont need aka "@"
        for tempPair in tempData:
            tempPair = tempPair.split("=")
            if tempPair[0] == "room-id" and tempPair[1] != '':
                roomID = tempPair[1]
                return roomID

    async def _decoded_send(self, data, loop,host,allData=None):
        """TODO: remove discord only features..."""  
        if data[1] == 'PRIVMSG':
            user = data[0].split('!')[0].lstrip(":")
            m = re.search(self.messagepattern, data[0])
            #meCheck = config.c.irc["Servers"][host]["Nickname"] == user
            message = ' '.join(data[3:])[1:]
            emojis = {}
            badges = {}
            if host == "irc.chat.twitch.tv":
                await self.twitchEmotes(message,allData,emojis)
                await self.twitchBadges(message,allData,badges)
                self.l.logger.info("TWITCH TAGS: " + allData)
            for emoteObj in self.emoteObjects:
                await emoteObj.getEmote(message,emojis,data[2])
            self.l.logger.info("Emotes: {0}".format(emojis))
            if m: #and not meCheck:
                self.l.logger.info("{0} - ".format(host) + data[2]+ ":" + user +': '+ message)
                msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":message,"sent":False}
                role = {}
                role.update({"Normal": 0})
                await self.processMsg(username=user,message=message,roleList=role,server=host,channel=data[2],emojis=emojis,badges=badges)
        elif data[1] == 'JOIN':
            user = data[0].split('!')[0].lstrip(":")
            self.l.logger.info("{0} - ".format(host)  + user+" joined")
            msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} joined the channel".format(user),"sent":False}
        elif data[1] == 'PART' or data[1] == 'QUIT':
            user = data[0].split('!')[0].lstrip(":")
            self.l.logger.info("{0} - ".format(host) + user+" left")
            msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} left the channel ({1})".format(user,data[3]),"sent":False}
        elif data[1] == 'NOTICE':
            pass
        elif data[1] == 'KICK':
            self.l.logger.info("{0} - ".format(host) + "I was kicked")
            self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
            await asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()
        elif data[1] == 'RECONNECT':
            self.l.logger.info("{0} - ".format(host) + "Reconnecting")
            self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
            await asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()

        elif data[0] == "ERROR":
            if ' '.join([data[1],data[2]]) == ":Closing link:":
                self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
                #print("[Twitch] Lost Connection or disconnected: %s" % ' '.join(data[4:]))
                self.l.logger.info("{0} - ".format(host) + "Lost connection")
                await asyncio.sleep(10)
                await self.ircConnect(loop,host)
                loop.stop()
                
                
    async def sendMSG(self,sndMessage): #sends messages to youtube live chat
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "irc": #determines if its the right service and supposed to be here 
            while self.serviceStarted[sndMessage.DeliveryDetails.Server] != True:
                await asyncio.sleep(0.2)
            #print(await sndMessage.DeliveryDetails.Channel,messageFormatter.formatter(sndMessage))
            msg = await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)
            #print(sndMessage.DeliveryDetails.Server)
            self.writer[sndMessage.DeliveryDetails.Server].write("PRIVMSG {0} :{1}".format(sndMessage.DeliveryDetails.Channel,msg).encode("utf-8") + b'\r\n')

        
#this starts everything for the irc client 
##possibly could of put all this in a class and been done with it?
def ircStart():
    IRC = irc()
    if config.c.irc["Enabled"] == True:
        loop = asyncio.get_event_loop()
        loop.create_task(IRC.irc_bot(loop))



# def ircCheck():
#     global config
#     ircThread = threading.Thread(target=ircStart) #creates the thread for the irc client
#     ircThread.start() #starts the irc bot
#     time.sleep(10)
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
        
ircStart()