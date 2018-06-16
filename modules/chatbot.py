from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger



class chatbot:
    def __init__(self):
        self.l = logger.logs("Chatbot")
        self.l.logger.info("Starting")
        config.events.onMessage += self.sortMessage
        self.l.logger.info("Started")

    async def sortMessage(self,message):
        self.l.logger.info(message.__dict__)
        for key ,val in config.chatbot.items():
            if message.Service == val["From"]["Service"]:
                if message.Server == val["From"]["Server"]:
                    if message.Channel == val["From"]["Channel"]:
                        self.l.logger.info('Send Message')
                        objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(ModuleTo=val["To"]["Module"],Service=val["To"]["Service"], Server=val["To"]["Server"],Channel=val["To"]["Channel"])
                        message.Contents = await self.serviceIdentifier(fromService=message.Service,fromServer=message.Server,fromChannel=message.Channel,toService=val["To"]["Service"],toServer=val["To"]["Server"],toChannel=val["To"]["Channel"],message=message.Contents)
                        await self.sendMessage(message=message,objDeliveryDetails=objDeliveryDetails)

                        

    async def serviceIdentifier(self,fromService,fromServer,fromChannel,toService,toServer,toChannel,message):
        for key ,val in config.chatbotIdentifier.items():
            if val["To"]["Service"] == toService and val["From"]["Service"] == fromService:
                if val["To"]["Server"] == toServer and val["From"]["Server"] == fromServer:
                    if val["To"]["Channel"] == toChannel and val["From"]["Channel"] == fromChannel:
                        return "{0} {1}".format(val["Format"],message)
        return message



    async def sendMessage(self,message,objDeliveryDetails):
        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails)

        config.events.onMessageSend(sndMessage=objSendMsg)
        pass