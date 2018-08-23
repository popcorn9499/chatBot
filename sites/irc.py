import asyncio
import re

from utils import config
from utils import Object
from utils import logger
from utils import messageFormatter

import time

##this is the event loop for the irc client
class irc():#alot of this code was given to me from thehiddengamer then i adapted to more of what i needed
    def __init__(self):
        self.messagepattern = re.compile(r"^:(.{1,50})!")
        #variables.config = __main__.variables.config
        self.l = logger.logs("IRC")
        self.l.logger.info("Starting")
        self.serviceStarted = True
        config.events.onMessageSend += self.sendMSG
        self.writer = {}
        self.reader = {}
    
    async def irc_bot(self, loop): #this all works, well, except for when both SweetieBot and SweetieBot_ are used. -- prints will be removed once finished, likely.        
        for sKey, sVal in config.irc["Servers"].items():
            host = sKey
            print(type(host))
            self.l.logger.info("{0} - Connecting".format(host)) 
            await self.ircConnect(loop,host)
        asyncio.sleep(3)
        self.l.logger.info("Connected: " + host)
            
    async def ircConnect(self,loop,host):#handles the irc connection
        self.readerBasic, self.writerBasic = await asyncio.open_connection(host,config.irc["Servers"][host]["Port"], loop=loop)
        self.reader.update({host: self.readerBasic})
        self.writer.update({host: self.writerBasic})
        #print(self.reader)
        #print(self.writer)
        self.l.logger.debug("{0} - Reader {1} ".format(host,self.reader))
        self.l.logger.debug("{0} - Writer {1} ".format(host, self.writer))
        await asyncio.sleep(3)
        if config.irc["Servers"][host]["Password"] != "":
            self.writer[host].write(b'PASS ' + config.irc["Servers"][host]["Password"].encode('utf-8') + b'\r\n')
            self.l.logger.info("{0} - Inputing password ".format(host)) #,"Info")
        self.l.logger.info("{0} - Setting user {1}+ ".format(host,config.irc["Servers"][host]["Nickname"]))
        self.writer[host].write(b'NICK ' + config.irc["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
        self.l.logger.info("{0} - Setting user {1}".format(host,config.irc["Servers"][host]["Nickname"]))
        self.writer[host].write(b'USER ' + config.irc["Servers"][host]["Nickname"].encode('utf-8') + b' B hi :' + config.irc["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
        await asyncio.sleep(3)
        self.l.logger.info("{0} - Joining channels".format(host))
        for key, val in config.irc["Servers"][host]["Channel"].items():
            print(key)
            self.writer[host].write(b'JOIN ' + key.encode('utf-8')+ b'\r\n')
            self.l.logger.info("{0} - Joining channel {1}".format(host,key))
        await asyncio.sleep(3)
        self.l.logger.info("{0} - Initiating IRC Reader".format(host))
        loop.create_task(self.handleMsg(loop,host)) 
                   
       
            
    async def handleMsg(self,loop,host):
        info_pattern = re.compile(r'00[1234]|37[526]|CAP')
        await asyncio.sleep(1)
        while True:
            if host in self.reader:
                try:
                    data = (await self.reader[host].readuntil(b'\n')).decode("utf-8")
                    data = data.rstrip()
                    data = data.split()
                    self.l.logger.info(' '.join(data) + host) #,"Extra Debug")
                    if data[0].startswith('@'): 
                        data.pop(0)
                    if data == []:
                        pass
                    elif data[0] == 'PING':
                        self.writer[host].write(b'PONG %s\r\n' % data[1].encode("utf-8"))
                    # elif data[0] == ':user1.irc.popicraft.net' or data[0] ==':irc.popicraft.net' or info_pattern.match(data[1]):
                        # print('[Twitch] ', ' '.join(data))
                        #generally not-as-important info
                    else:
                        print(data)
                        await self._decoded_send(data, loop,host)
                except asyncio.streams.IncompleteReadError:
                    pass
            else:
                print("{0} doesnt exist".format(host))

                
    
    async def processMsg(self,username,message,roleList,server,channel):
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": "irc","%message%":"message"}
        message = await Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service="irc",Roles=roleList)
        objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions)
        config.events.onMessage(message=objSendMsg)
        
    
    async def _decoded_send(self, data, loop,host):
        """TODO: remove discord only features..."""
        
        if data[1] == 'PRIVMSG':
            user = data[0].split('!')[0].lstrip(":")
            m = re.search(self.messagepattern, data[0])
            if m:
                message = ' '.join(data[3:]).strip(':').split()
                self.l.logger.info("{0} - ".format(host) + data[2]+ ":" + user +': '+ ' '.join(message))
                msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":' '.join(message),"sent":False}
                role = {}
                role.update({"Normal": 0})
                await self.processMsg(username=user,message=' '.join(message),roleList=role,server=host,channel=data[2])
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
            asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()
        elif data[1] == 'RECONNECT':
            self.l.logger.info("{0} - ".format(host) + "Reconnecting")
            self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
            asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()

        elif data[0] == "ERROR":
            if ' '.join([data[1],data[2]]) == ":Closing link:":
                self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
                #print("[Twitch] Lost Connection or disconnected: %s" % ' '.join(data[4:]))
                self.l.logger.info("{0} - ".format(host) + "Lost connection")
                asyncio.sleep(10)
                await self.ircConnect(loop,host)
                loop.stop()
                
                
    async def sendMSG(self,sndMessage): #sends messages to youtube live chat
        while self.serviceStarted != True:
            await asyncio.sleep(5)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "irc": #determines if its the right service and supposed to be here
            self.writer[sndMessage.DeliveryDetails.Server].write("PRIVMSG {0} :{1}".format(sndMessage.DeliveryDetails.Channel,await messageFormatter.formatter(sndMessage)).encode("utf-8") + b'\r\n')

        
#this starts everything for the irc client 
##possibly could of put all this in a class and been done with it?
def ircStart():
    loop = asyncio.get_event_loop()
    loop.create_task(irc().irc_bot(loop))


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