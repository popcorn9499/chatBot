from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger



class chatbot:
    def __init__(self):
        self.l = logger.logs("Commands")
        self.l.logger.info("Starting")
        config.events.onMessage += self.command1
        self.l.logger.info("Started")

    async def command1(self,message):
        rolesAllowed = ["Owner","Mod","Normal"]
        commandInfo1 = {"CommandType":"Message","Command":"!hi","CommandDetails":"Yes this should work!!","rolesAllowed":rolesAllowed}
        commands = [commandInfo1]
        if message.Message.Contents.startswith("!") == True:
            self.l.logger.info("Recieved")
            for command in commands:
                if message.Message.Contents.startswith(command["Command"]) == True:
                    if command["CommandType"] == "Message": 
                        for key, val in message.Message.Roles.items():
                            for keyAllowed in rolesAllowed:
                                if key == keyAllowed:
                                    self.l.logger.info(command["CommandDetails"])
                                    botRoles= {"":0}
                                    await self.processMsg(message=command["CommandDetails"],username="Bot",channel=message.Message.Channel,server=message.Message.Server,service=message.Message.Service,roleList=botRoles)
                            print("{0}: {1}".format(key,val))
    

    async def processMsg(self,username,message,roleList,server,channel,service):
        formatOptions = {"%authorName%": username, "%channelFrom%": channel, "%serverFrom%": server, "%serviceFrom%": service,"%message%":"message","%roles%":roleList}
        message = await Object.ObjectLayout.message(Author=username,Contents=message,Server=server,Channel=channel,Service=service,Roles=roleList)
        objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(Module="Command",ModuleTo="Site",Service=service,Server=server,Channel=channel)
        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions)
        config.events.onMessageSend(sndMessage=objSendMsg)     





chat = chatbot()