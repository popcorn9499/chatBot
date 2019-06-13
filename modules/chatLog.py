from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger
from utils import fileIO
import os


class chatLog:
    def __init__(self):
        self.l = logger.logs("ChatLog")
        self.l.logger.info("Starting")
        config.events.onMessage += self.logMessage
        self.l.logger.info("Started")
        fileIO.checkFolder("config{0}chatLog{0}".format(os.sep),"logRules",self.l)
        fileIO.checkFile("config-example{0}chatLog{0}logRules.json".format(os.sep),"config{0}chatLog{0}logRules.json".format(os.sep),"logRules.json",self.l)
        self.chatLogRules = fileIO.loadConf("config{0}chatLog{0}logRules.json")
        
    async def logMessage(self,message):
        self.l.logger.debug("Logging")
        self.l.logger.debug(message.DeliveryDetails.__dict__)
        self.l.logger.debug(message.Message.__dict__)
        if message.DeliveryDetails.Module == "Site":
            for key ,val in self.chatLogRules.items():
                isEnabled = await self.ifEnabled(key,val)            
                isIgnored = await self.checkIgnoreList(message.Message.Server,message.Message.Channel, message.Message.Service,val)
                if isEnabled and not isIgnored:
                    objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="ChatLog",ModuleTo="Site",Service=val["Service"], Server=val["Server"],Channel=val["Channel"]) #prepares the delivery location
                    await self.sendMessage(message=message.Message,objDeliveryDetails=objDeliveryDetails, FormattingOptions=message.FormattingOptions,messageUnchanged=message.messageUnchanged)

    async def checkIgnoreList(self,server,channel,service,val):
        if 'IgnoreList' in val:
            for item in val["IgnoreList"]:
                if item["Service"] == service and item["Server"] == server and item["Channel"] == channel:
                    return True
        return False


    async def ifEnabled(self,key,val): #checks if the logging is enabled. also adds the option if it doesn't already exist
        self.l.logger.info("Checking if enabled")
        if not 'Enabled' in val:
            self.l.logger.info("Missing")
            self.chatLogRules[key].update({"Enabled": True})
            fileIO.fileSave("config{0}chatLog{0}logRules.json".format(os.sep),self.chatLogRules)
        return val["Enabled"]

    async def sendMessage(self,message,objDeliveryDetails,FormattingOptions,messageUnchanged): #sends the message
        formatterOptions = {""}
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,messageUnchanged=messageUnchanged) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)


chatLog = chatLog()