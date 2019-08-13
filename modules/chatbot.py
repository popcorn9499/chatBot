from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger
from utils import fileIO
from modules import messageFilter
from utils import messageFormatter
import os



class chatbot:
    def __init__(self):
        self.l = logger.logs("Chatbot")
        self.l.logger.info("Starting")
        config.events.onMessage += self.sortMessage
        self.l.logger.info("Started")
        fileIO.checkFolder("config{0}chatbot{0}".format(os.sep),"chatbot",self.l)
        fileIO.checkFile("config-example{0}chatbot{0}chatbot.json".format(os.sep),"config{0}chatbot{0}chatbot.json".format(os.sep),"chatbot.json",self.l)
        self.chatbot =  fileIO.loadConf("config{0}chatbot{0}chatbot.json")
        
        self.legacyConverts()

    def legacyConverts(self):#converts tags from legacy portions of the code or removes them if unnessisary
        try:
            self.chatbotIdentifier = fileIO.loadConf("config{0}chatbot{0}chatbotIdentifier.json")
            self.chatbot["Identifier"] = self.chatbotIdentifier.pop("Format")
            filename = "config{0}chatbot{0}chatbotIdentifier.json".format(os.sep)
            fileIO.fileSave(filename,self.chatbotIdentifier)
        except:
            pass

    async def sortMessage(self,message): #sorts messages sending themto the correct locations
        self.l.logger.debug(message.__dict__) #more or less debug code
        formatOptions = message.FormattingOptions
        msg = message.Message
        for key ,val in self.chatbot.items(): #cycles through the config of options
            #message filtering
            if (await messageFilter.messageFilter.filterMessage(msg)):#exits abruptly if message is bad
                break
            
            if msg.Service == val["From"]["Service"]: #decides weather this is the correct message is to be filtered out.
                if msg.Server == val["From"]["Server"]:
                    if msg.Channel == val["From"]["Channel"]:
                        try:
                            formatType = "Other"
                            formattingSettings = val["Formatting"]
                        except KeyError:
                            formatType = "File"
                            formattingSettings = "default.json"
                        
                        self.l.logger.debug('Sent Message')
                        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Chatbot",ModuleTo=val["To"]["Module"],Service=val["To"]["Service"], Server=val["To"]["Server"],Channel=val["To"]["Channel"]) #prepares the delivery location
                        ServiceIcon = await self.serviceIdentifier(fromService=msg.Service,fromServer=msg.Server,fromChannel=msg.Channel,toService=val["To"]["Service"],toServer=val["To"]["Server"],toChannel=val["To"]["Channel"],message=msg.Contents) #sees if it needs to be identified
                        formatOptions.update({"%serviceIcon%": ServiceIcon}) #Adds more formatting options
                        

                        if val["To"]["Service"].find("-Webhook") == -1:
                            self.l.logger.info("No Webook")
                            webhookSupport=False
                        else: #webhook exists
                            webhookSupport=True
                            if "AuthorFormatting" in val:
                                authorFormatting = val["AuthorFormatting"]
                                msg.Author = await messageFormatter._formatter(msg.Author,formatOptions,formattingOptions=authorFormatting,formatType="Other")
                            else:
                                msg.Author = ServiceIcon + " " + msg.Author
                            self.l.logger.info("Sending Webook")

                        await self.sendMessage(message=msg,objDeliveryDetails=objDeliveryDetails,FormattingOptions=formatOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message)#.messageUnchanged) #sends the message

                        

    async def serviceIdentifier(self,fromService,fromServer,fromChannel,toService,toServer,toChannel,message): #adds a smaller easier identifier to the messages
        for key ,val in self.chatbot.items(): #cycles through everything to eventually possibly find a match
            if val["To"]["Service"] == toService and val["From"]["Service"] == fromService:
                if val["To"]["Server"] == toServer and val["From"]["Server"] == fromServer:
                    if val["To"]["Channel"] == toChannel and val["From"]["Channel"] == fromChannel:
                        if "Identifier" in val:
                            return "{0}".format(val["Identifier"])#formats the message potentially
                        else: #return empty string if Identifier does not exist
                            return ""
        return "" #returns nothing if all else fails


    async def sendWebhook(self,message,objDeliveryDetails,FormattingOptions,formattingSettings,formatType,messageUnchanged): #sends the message
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onWebhookSend(sndMessage=objSendMsg)

    async def sendMessage(self,message,objDeliveryDetails,FormattingOptions,formattingSettings,formatType,messageUnchanged): #sends the message
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)

chatbot = chatbot()