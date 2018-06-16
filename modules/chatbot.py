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
                        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message.Message, DeliveryDetails=objDeliveryDetails)
                        print(objSendMsg)
                        config.events.onMessageSend(sndMessage=objSendMsg)

    async def sendMessage(self,message):
        pass