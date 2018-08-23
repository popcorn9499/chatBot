import asyncio
class _EventHook(object):
    def __init__(self):
        self.__handlers = []
    def __iadd__(self, handler): # ex: onMessage += callback
        self.__handlers.append(handler)
        return self
    def __isub__(self, handler): # ex: onMessage -= callback
        self.__handlers.remove(handler)
        return self
    def __call__(self, *args, **keywargs): # ex: onMessage()
        for handler in self.__handlers:
            asyncio.get_event_loop().create_task(handler(*args, **keywargs))

class test:
    def __init__(self):
        self.onConnect = _EventHook()
        self.onConnect += self.why
        self.onRaw = _EventHook()


    async def why(self,y):
        print("hello")
        print(y)


async def whynot():
    for i in range(123):
        test1.onConnect("test")
    await asyncio.sleep(0.001)
    asyncio.get_event_loop().stop

test1 = test()
test1.onConnect("test")
asyncio.get_event_loop().run_until_complete(whynot())

# import variables
# import asyncio
# import re
# import threading
# import time



# import json

# #file load and save stuff
# def fileSave(fileName,config):
#     print("Saving")
#     f = open(fileName, 'w') #opens the file your saving to with write permissions
#     f.write(json.dumps(config,sort_keys=True, indent=4 ) + "\n") #writes the string to a file
#     f.close() #closes the file io

# def fileLoad(fileName):#loads files
#     with open(fileName, 'r') as handle:#loads the json file
#         config = json.load(handle) 
#     return config

# variables.config = fileLoad("config-test.json")



# ##this is the event loop for the irc client
# class irc():#alot of this code was given to me from thehiddengamer then i adapted to more of what i needed
#     def __init__(self):
#         self.messagepattern = re.compile(r"^:(.{1,50})!")
#         #variables.config = __main__.variables.config
#         self.writer = {}
#         self.reader = {}
#         self.onConnect = _EventHook()
#         self.onRaw = _EventHook()
#         self.onRaw += self._decoded_send
#         self.onRaw += self.rawMsgRcvd
    
#     async def addConesole(self,msg,host,errorLevel):
#         print("{0} {1} {2}".format(msg,host,errorLevel))

#     async def irc_bot(self, loop): #this all works, well, except for when both SweetieBot and SweetieBot_ are used. -- prints will be removed once finished, likely.
#         #host = variables.config["Bot"]["IRC"]["IP"]
        
#         for sKey, sVal in variables.config["Bot"]["IRC"]["Servers"].items():
#             host = sKey
#             await self.addConesole("Connecting",host,"Info")
#             await self.ircConnect(loop,host)
#         asyncio.sleep(3)
#         loop.create_task(self.handleSendMsg(loop))
#         await self.addConesole("Connected",host,"Info")
#         print(self.reader)
#         print(self.writer)
            
#     async def ircConnect(self,loop,host):#handles the irc connection
#         self.readerBasic, self.writerBasic = await asyncio.open_connection(host,variables.config["Bot"]["IRC"]["Servers"][host]["Port"], loop=loop)
#         self.reader.update({host: self.readerBasic})
#         self.writer.update({host: self.writerBasic})
#         print(self.reader)
#         print(self.writer)
#         await self.addConesole("Reader {0}".format(self.reader),host,"Extra Debug")
#         await self.addConesole("Writer {0}".format(self.writer),host,"Extra Debug")
#         await asyncio.sleep(3)
#         if variables.config["Bot"]["IRC"]["Servers"][host]["Password"] != "":
#             self.writer[host].write(b'PASS ' + variables.config["Bot"]["IRC"]["Servers"][host]["Password"].encode('utf-8') + b'\r\n')
#             await self.addConesole("Inputing password",host,"Info")

#         await self.addConesole("Setting user {0}".format(variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"]),host,"Debug")

        
#         self.writer[host].write(b'NICK ' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
#         await self.addConesole("Setting user {0}".format(variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"]),host,"Extra Info")
#         self.writer[host].write(b'USER ' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b' B hi :' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
#         await asyncio.sleep(3)
#         await self.addConesole("Joining channels",host,"Info")
#         for key, val in variables.config["Bot"]["IRC"]["Servers"][host]["Channel"].items():
#             print(key)
#             self.writer[host].write(b'JOIN ' + key.encode('utf-8')+ b'\r\n')
#             await self.addConesole("Joining channel {0}".format(key),host,"Info")
#         await asyncio.sleep(3)
#         await self.addConesole("Initiating IRC Reader",host,"Debug")
#         loop.create_task(self.handleMsg(loop,host)) 
        
#     async def handleSendMsg(self,loop):
#         #irc msg handler
#         while True:
#             j = 0

#             for msg in variables.processedMSG: #this cycles through the array for messages unsent to irc and sends them
#                 if msg["sent"] == False and msg["sendTo"]["Bot"] == "IRC":
#                     await self.sendMSG(msg["sendTo"]["Server"],msg["sendTo"]["Channel"],msg["msgFormated"])
#                     #sends the message to the irc from whatever
#                     variables.processedMSG[j]["sent"] = True#promptly after sets that to the delete code
#                 j = j + 1
#             await asyncio.sleep(1)
            
       
            
#     async def handleMsg(self,loop,host):
#         info_pattern = re.compile(r'00[1234]|37[526]|CAP')
#         await asyncio.sleep(1)
#         while True:
#             if host in self.reader:
#                 try:
#                     data = (await self.reader[host].readuntil(b'\n')).decode("utf-8")
#                     data = data.rstrip()
#                     data = data.split()
#                     await self.addConesole(' '.join(data),host,"Extra Debug")
#                     if data[0].startswith('@'): 
#                         data.pop(0)
#                     if data == []:
#                         pass
#                     elif data[0] == 'PING':
#                         self.writer[host].write(b'PONG %s\r\n' % data[1].encode("utf-8"))
#                     # elif data[0] == ':user1.irc.popicraft.net' or data[0] ==':irc.popicraft.net' or info_pattern.match(data[1]):
#                         # print('[Twitch] ', ' '.join(data))
#                         #generally not-as-important info
#                     else:
#                         print(data)
#                         #await self._decoded_send(data, loop,host)
#                         self.onRaw(data,loop,host)
#                 except asyncio.streams.IncompleteReadError:
#                     x = 1
#             else:
#                 print("{0} doesnt exist".format(host))

                
    
#     async def rawMsgRcvd(self, *args, **kwargs):
#         print("HI HELLO LMAO")

        
    
#     async def _decoded_send(self, data, loop,host):
#         """TODO: remove discord only features..."""
#         if data[1] == 'PRIVMSG':
#             user = data[0].split('!')[0].lstrip(":")
#             m = re.search(self.messagepattern, data[0])
#             if m:
#                 message = ' '.join(data[3:]).strip(':').split()
#                 await self.addConesole(data[2]+ ":" + user +': '+ ' '.join(message),host,"Info")
#                 msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":' '.join(message),"sent":False}
#                 variables.mainMsg.append(msgStats)
#         elif data[1] == 'JOIN':
#             user = data[0].split('!')[0].lstrip(":")
#             #temp
#             await self.addConesole(user+" joined",host,"Info")
#             msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} joined the channel".format(user),"sent":False}
#             variables.mainMsg.append(msgStats)
#             x = 1
#         elif data[1] == 'PART' or data[1] == 'QUIT':
#             user = data[0].split('!')[0].lstrip(":")
#             await self.addConesole(user+" left",host,"Info")
#             msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} left the channel ({1})".format(user,data[3]),"sent":False}
#             variables.mainMsg.append(msgStats)
#             #temp
#             x = 1
#         elif data[1] == 'NOTICE':
#             #temp
#             x = 1
#         elif data[1] == 'KICK':
#             print('[Twitch] ', 'Twitch has requested that I reconnect, This is currently unsupported.')
#             await self.addConesole("I was kicked",host,"Info")
#             self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
#             asyncio.sleep(10)
#             await self.ircConnect(loop,host)
#             loop.stop()
#         elif data[1] == 'RECONNECT':
#             await self.addConesole("Reconnecting",host,"Info")
#             self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
#             asyncio.sleep(10)
#             await self.ircConnect(loop,host)
#             loop.stop()

#         elif data[0] == "ERROR":
#             if ' '.join([data[1],data[2]]) == ":Closing link:":
#                 self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
#                 print("[Twitch] Lost Connection or disconnected: %s" % ' '.join(data[4:]))
#                 await self.addConesole("Lost connection",host,"Info")
#                 asyncio.sleep(10)
#                 await self.ircConnect(loop,host)
#                 loop.stop()
                
                
#     async def sendMSG(self,server,channel, msg):
#         self.writer[server].write("PRIVMSG {0} :{1}".format(channel,msg).encode("utf-8") + b'\r\n')

        
# #this starts everything for the irc client 
# ##possibly could of put all this in a class and been done with it?
# def ircStart():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.create_task(irc().irc_bot(loop))
#     loop.run_forever()
#     loop.close()

# #ircStart()
        
