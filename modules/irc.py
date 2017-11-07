import asyncio
import re
from modules import variables
from modules import mainBot


##this is the event loop for the irc client
class irc():#alot of this code was given to me from a friend then i adapted to more of what i needed
    def __init__(self):
        self.messagepattern = re.compile(r"^:(.{1,50})!")
        #variables.config = __main__.variables.config
        self.writer = {}
        self.reader = {}
    
    async def irc_bot(self, loop): #this all works, well, except for when both SweetieBot and SweetieBot_ are used. -- prints will be removed once finished, likely.
        #host = variables.config["Bot"]["IRC"]["IP"]
        
        for sKey, sVal in variables.config["Bot"]["IRC"]["Servers"].items():
            host = sKey
            await mainBot.mainBot().addConsoleAsync("Connecting",host,"Info")
            await self.ircConnect(loop,host)
            #loop.create_task(Twitch_boT.handleMsg(loop,"irc.chat.twitch.tv"))
        
            #writer.write(b'JOIN #' + "test".encode('utf-8')+ b'\r\n')
            #writer.write("PRIVMSG #test :mods".encode('utf-8')+ b'\r\n')
        asyncio.sleep(3)
        loop.create_task(self.handleSendMsg(loop))
        await mainBot.mainBot().addConsoleAsync("Connected",host,"Info")
        print(self.reader)
        print(self.writer)
            
    async def ircConnect(self,loop,host):#handles the irc connection
        self.readerBasic, self.writerBasic = await asyncio.open_connection(host,variables.config["Bot"]["IRC"]["Servers"][host]["Port"], loop=loop)
        self.reader.update({host: self.readerBasic})
        self.writer.update({host: self.writerBasic})
        print(self.reader)
        print(self.writer)
        await mainBot.mainBot().addConsoleAsync("Reader {0}".format(self.reader),host,"Extra Debug")
        await mainBot.mainBot().addConsoleAsync("Writer {0}".format(self.writer),host,"Extra Debug")
        await asyncio.sleep(3)
        if variables.config["Bot"]["IRC"]["Servers"][host]["Password"] != "":
            self.writer[host].write(b'PASS ' + variables.config["Bot"]["IRC"]["Servers"][host]["Password"].encode('utf-8') + b'\r\n')
            await mainBot.mainBot().addConsoleAsync("Inputing password",host,"Info")

        await mainBot.mainBot().addConsoleAsync("Setting user {0}".format(variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"]),host,"Debug")

        
        self.writer[host].write(b'NICK ' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
        await mainBot.mainBot().addConsoleAsync("Setting user {0}".format(variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"]),host,"Extra Info")
        self.writer[host].write(b'USER ' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b' B hi :' + variables.config["Bot"]["IRC"]["Servers"][host]["Nickname"].encode('utf-8') + b'\r\n')
        await asyncio.sleep(3)
        await mainBot.mainBot().addConsoleAsync("Joining channels",host,"Info")
        for key, val in variables.config["Bot"]["IRC"]["Servers"][host]["Channel"].items():
            print(key)
            self.writer[host].write(b'JOIN ' + key.encode('utf-8')+ b'\r\n')
            await mainBot.mainBot().addConsoleAsync("Joining channel {0}".format(key),host,"Info")
        await asyncio.sleep(3)
        await mainBot.mainBot().addConsoleAsync("Initiating IRC Reader",host,"Debug")
        loop.create_task(self.handleMsg(loop,host)) 
        
    async def handleSendMsg(self,loop):
        #irc msg handler
        while True:
            j = 0
            #print("lo")
            for msg in variables.processedMSG: #this cycles through the array for messages unsent to irc and sends them
                #print(msg["sendTo"])
                if msg["sent"] == False and msg["sendTo"]["Bot"] == "IRC":
                    #print(msg["msgFormated"])
                    #self.writer.write(b'PRIVMSG #test '+b' :' + msg["msgFormated"].encode("utf-8") + b'\r\n')
                    await self.sendMSG(msg["sendTo"]["Server"],msg["sendTo"]["Channel"],msg["msgFormated"])
                    #sends the message to the irc from whatever
                    variables.processedMSG[j]["sent"] = True#promptly after sets that to the delete code
                j = j + 1
            await asyncio.sleep(1)
            
       
            
    async def handleMsg(self,loop,host):
        info_pattern = re.compile(r'00[1234]|37[526]|CAP')
        await asyncio.sleep(1)
        while True:
            if host in self.reader:
                try:
                    data = (await self.reader[host].readuntil(b'\n')).decode("utf-8")
                    data = data.rstrip()
                    data = data.split()
                    await mainBot.mainBot().addConsoleAsync(' '.join(data),host,"Extra Debug")
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
                    x = 1
            else:
                print("{0} doesnt exist".format(host))
                #for sKey, sVal in variables.config["Bot"]["IRC"]["Servers"].items(): 
                    # this should check to see if the host or ip was used and initialized before trying to read from it
                
    

        
    
    async def _decoded_send(self, data, loop,host):
        """TODO: remove discord only features..."""
        
        if data[1] == 'PRIVMSG':
            user = data[0].split('!')[0].lstrip(":")
            m = re.search(self.messagepattern, data[0])
            if m:
                message = ' '.join(data[3:]).strip(':').lower().split()
                await mainBot.mainBot().addConsoleAsync(data[2]+ ":" + user +': '+ ' '.join(message),host,"Info")
                msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":' '.join(message),"sent":False}
                variables.mainMsg.append(msgStats)
                # if message[0] == '!' + variables.config['Twitch']['command']:
                    # link = message[1]
                    # # print('Command seen: ', message, link if self._check_if_osu(link) else 'False')
                    # # if self._check_if_osu(link):
                        # # await Osu_bot.send_osu_link(link)

                # if message[0] == '!shutdownosu':
                    # loop.stop()
        elif data[1] == 'JOIN':
            user = data[0].split('!')[0].lstrip(":")
            #temp
            await mainBot.mainBot().addConsoleAsync(user+" joined",host,"Info")
            msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} joined the channel".format(user),"sent":False}
            variables.mainMsg.append(msgStats)
            x = 1
        elif data[1] == 'PART' or data[1] == 'QUIT':
            user = data[0].split('!')[0].lstrip(":")
            await mainBot.mainBot().addConsoleAsync(user+" left",host,"Info")
            msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": data[2], "author": user,"authorData": None,"authorsRole": {"Normal": 0},"msg":"{0} left the channel ({1})".format(user,data[3]),"sent":False}
            variables.mainMsg.append(msgStats)
            #temp
            x = 1
        elif data[1] == 'NOTICE':
            #temp
            x = 1
        elif data[1] == 'KICK':
            print('[Twitch] ', 'Twitch has requested that I reconnect, This is currently unsupported.')
            await mainBot.mainBot().addConsoleAsync("I was kicked",host,"Info")
            self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
            asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()
        elif data[1] == 'RECONNECT':
            await mainBot.mainBot().addConsoleAsync("Reconnecting",host,"Info")
            self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
            asyncio.sleep(10)
            await self.ircConnect(loop,host)
            loop.stop()

        elif data[0] == "ERROR":
            if ' '.join([data[1],data[2]]) == ":Closing link:":
                self.writer[host].write('QUIT Bye \r\n'.encode("utf-8"))
                print("[Twitch] Lost Connection or disconnected: %s" % ' '.join(data[4:]))
                await mainBot.mainBot().addConsoleAsync("Lost connection",host,"Info")
                asyncio.sleep(10)
                await self.ircConnect(loop,host)
                loop.stop()
                
                
    async def sendMSG(self,server,channel, msg):
        #print("sending")
        self.writer[server].write("PRIVMSG {0} :{1}".format(channel,msg).encode("utf-8") + b'\r\n')
