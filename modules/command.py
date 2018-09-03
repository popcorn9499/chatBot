from utils import config
from utils import Object
import asyncio
import time
import datetime
import os
from utils import logger
from utils import fileIO


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
        self.commands = []
        self.commandsDir = '.{0}config{0}command'.format(os.sep)
        self.checkCommandFolder()
        self.loadCommands()
        self.l.logger.info("Started")

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
        if command["CommandType"] == "Message" and await self.commandRoleChecker(message=message,command=command) == True: 
            await self.commandMessage(message=message,command=command)
        elif command["CommandType"] == "FileRead" and await self.commandRoleChecker(message=message,command=command) == True: 
            await self.commandFileRead(message=message,command=command)
        elif command["CommandType"] == "CloseBot" and await self.commandRoleChecker(message=message,command=command) == True: 
            await self.commandClose(message=message,command=command)
        elif command["CommandType"] == "ReloadModules" and await self.commandRoleChecker(message=message,command=command) == True: 
            await self.commandReloadModules(message=message,command=command)
        elif command["CommandType"] == "Help" and await self.commandRoleChecker(message=message,command=command) == True: 
            await self.commandHelp(message=message,command=command)
                

    async def commandRoleChecker(self,message,command):
        for key, val in message.Message.Roles.items():
            for keyAllowed in command["RolesAllowed"]:
                if key == keyAllowed:
                    return True
        return False
                        

    async def commandHelp(self,message,command):
        commandOutput = "``` \r\n"
        commandOutput = "{0}READDDD \r\n".format(command)
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




    

    async def processMsg(self,username,message,roleList,server,channel,service):
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": service,"%message%":"message","%roles%":roleList}
        message = await Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service=service,Roles=roleList)
        objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(Module="Command",ModuleTo="Site",Service=service,Server=server,Channel=channel)
        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions)
        config.events.onMessageSend(sndMessage=objSendMsg)     





chat = Commands()