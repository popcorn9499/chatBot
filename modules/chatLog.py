from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger



class chatLog:
    def __init__(self):
        self.l = logger.logs("ChatLog")
        self.l.logger.info("Starting")
        config.events.onMessage += self.logMessage
        self.l.logger.info("Started")
        
    async def logMessage(self,message):
        print(message.DeliveryDetails.__dict__)
        print(message.Message.__dict__)
        if message.DeliveryDetails.Module == "Site":
            for key ,val in config.chatLogRules.items():
                objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(Module="ChatLog",ModuleTo="Site",Service=val["Service"], Server=val["Server"],Channel=val["Channel"]) #prepares the delivery location
                await self.sendMessage(message=message.Message,objDeliveryDetails=objDeliveryDetails, FormattingOptions=message.FormattingOptions)
            pass


    async def sendMessage(self,message,objDeliveryDetails,FormattingOptions): #sends the message
        formatterOptions = {""}
        objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)


