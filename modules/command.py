from utils import config
from utils import Object
import asyncio
import time
import datetime
import os
from utils import logger
from utils import fileIO
from utils.EventHook import EventHook

#Commands to add
#-Get Viewer Count?
#-Set Stream Title (Twitch Youtube)
#-Set Stream Game (Twitch Youtube?)
#-mute user (irc wouldnt work sadly. Twitch should..)
#-Unmute user (IRC /|\)
#-Increment File
#-Time Live
#-Ban User
#-Kick User
#-Help



class Commands:
    def __init__(self):
        self.l = logger.logs("Commands")
        self.l.logger.info("Starting")
        config.events.onMessage += self.commandCheckExist
        config.events.addCommandType = EventHook()
        config.events.addCommandType += self.addCommandTypes
        self.commands = []
        self.commandTypeList = {}
        self.commandsDir = '.{0}config{0}command'.format(os.sep)
        self.checkCommandFolder()
        self.loadCommands()
        loop = asyncio.get_event_loop()
        loop.create_task(self.addBasicCommands())
        self.l.logger.info("Started")
    
    async def addBasicCommands(self):
        config.events.addCommandType(commandType="Help",commandHandler=self.commandHelp)
        config.events.addCommandType(commandType="Message",commandHandler=self.commandMessage)
        config.events.addCommandType(commandType="FileRead",commandHandler=self.commandFileRead)
        config.events.addCommandType(commandType="CloseBot",commandHandler=self.commandClose)
        config.events.addCommandType(commandType="ReloadModules",commandHandler=self.commandClose)
        config.events.addCommandType(commandType="DeleteByMsgDetails",commandHandler=self.commandClose)



    async def addCommandTypes(self,commandType,commandHandler):
        print(commandType)
        self.commandTypeList.update({commandType:EventHook()})
        self.commandTypeList[commandType] += commandHandler

    def checkCommandFolder(self):
        if os.path.isdir(self.commandsDir) == False:
            self.l.logger.info("Commands Folder Does Not Exist")
            self.l.logger.info("Creating...")
            os.makedirs(self.commandsDir)

    def loadCommands(self):
        for dirname, dirnames,filenames in os.walk(self.commandsDir):
            for filename in filenames:
                print("{1}{0}{2}".format(os.sep,dirname,filename))
                self.commands.append(fileIO.fileLoad("{1}{0}{2}".format(os.sep,dirname,filename)))




    async def commandCheckExist(self,message):
        if message.Message.Contents.startswith("!") == True:
            self.l.logger.info("Recieved")
            for command in self.commands:
                if message.Message.Contents.startswith(command["Command"]) == True:
                    await self.commandTypeCheck(message=message,command=command)
                    

                    
    
    async def commandTypeCheck(self,message,command):
        for key,val in self.commandTypeList.items():
            if (command["CommandType"] == key) & (await self.commandRoleChecker(message=message,command=command) == True):
                self.commandTypeList[key](message=message,command=command)
       
                

    async def commandRoleChecker(self,message,command):
        for key, val in message.Message.Roles.items():
            for keyAllowed in command["RolesAllowed"]:
                if key == keyAllowed:
                    return True
        return False
                        

    async def commandHelp(self,message,command):
        commandOutput = "``` \r\n"
        #commandOutput = "{0}READDDD \r\n".format(command)
        for com in self.commands:
            commandOutput = "{0} \r\n {1}: {2}".format(commandOutput,com["Command"], com["HelpDetails"])
        commandOutput = "{0} \r\n ```".format(commandOutput)
        botRoles= {"":0}
        await self.processMsg(message=commandOutput,username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)


    async def commandMessage(self,message,command):
        self.l.logger.info(command["CommandDetails"])
        botRoles= {"":0}
        await self.processMsg(message=command["CommandDetails"],username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)


    async def commandFileRead(self,message,command):
        self.l.logger.info(command["CommandDetails"])
        botRoles= {"":0}
        f = open(command["CommandDetails"], 'r')#opens file
        await self.processMsg(message=f.read(),username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)
        f.close()

    async def commandClose(self,message,command):
        self.l.logger.info(command["CommandDetails"])
        botRoles= {"":0}
        self.l.logger.info("Not Implemented")
        await self.processMsg(message=command["CommandDetails"],username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)

    async def commandReloadModules(self,message,command):
        self.l.logger.info(command["CommandDetails"])
        botRoles= {"":0}
        self.l.logger.info("Not Implemented")
        await self.processMsg(message=command["CommandDetails"],username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)

    async def commandDeleteMsgByDetails(self,message,command):
        msgSplit = message.Message.Contents.split(" ")
        



    

    async def processMsg(self,username,message,roleList,server,channel,service):
        print("ya... {0}".format(message))
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": service,"%message%":"message","%roles%":roleList}
        message = Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service=service,Roles=roleList)
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Command",ModuleTo="Site",Service=service,Server=server,Channel=channel)
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged="None")
        config.events.onMessageSend(sndMessage=objSendMsg)     





commandChat = Commands()