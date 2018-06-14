from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger



class chatbot:
    def __init__(self):
        self.l = logger.logs("Chatbot")
        self.l.logger.info("test")
        config.events.onMessage += self.sortMessage

    async def sortMessage(self,message):
        self.l.logger.info(message.__dict__)
        if message.Author != "PopicraftTest": #this code should be modified
            if message.Channel != "log": #this code should be modified
                for key ,val in config.chatbot.items():
                    if message.Service == val["From"]["Service"]:
                        if message.Server == val["From"]["Server"]:
                            if message.Channel == val["From"]["Channel"]:
                                print("Sorted")
                                objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(ModuleTo=val["To"]["Module"],Service=val["To"]["Service"], Server=val["To"]["Server"],Channel=val["To"]["Channel"])
                                objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails)
                                print(objSendMsg)
                                config.events.onMessageSend(sndMessage=objSendMsg)

    async def sendMessage(self,message):
        pass