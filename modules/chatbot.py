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

    async def sortMessage(self,message): #sorts messages sending themto the correct locations
        self.l.logger.debug(message.__dict__) #more or less debug code
        formatOptions = message.FormattingOptions
        msg = message.Message
        for key ,val in config.chatbot.items(): #cycles through the config of options
            if msg.Service == val["From"]["Service"]: #decides weather this is the correct message matching it to the config
                if msg.Server == val["From"]["Server"]:
                    if msg.Channel == val["From"]["Channel"]:
                        self.l.logger.debug('Sent Message')
                        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Chatbot",ModuleTo=val["To"]["Module"],Service=val["To"]["Service"], Server=val["To"]["Server"],Channel=val["To"]["Channel"]) #prepares the delivery location
                        ServiceIcon = await self.serviceIdentifier(fromService=msg.Service,fromServer=msg.Server,fromChannel=msg.Channel,toService=val["To"]["Service"],toServer=val["To"]["Server"],toChannel=val["To"]["Channel"],message=msg.Contents) #sees if it needs to be identified
                        formatOptions.update({"%serviceIcon%": ServiceIcon}) #Adds more formatting options
                        await self.sendMessage(message=msg,objDeliveryDetails=objDeliveryDetails,FormattingOptions=formatOptions,messageUnchanged=message)#.messageUnchanged) #sends the message

                        

    async def serviceIdentifier(self,fromService,fromServer,fromChannel,toService,toServer,toChannel,message): #adds a smaller easier identifier to the messages
        for key ,val in config.chatbotIdentifier.items(): #cycles through everything to eventually possibly find a match
            if val["To"]["Service"] == toService and val["From"]["Service"] == fromService:
                if val["To"]["Server"] == toServer and val["From"]["Server"] == fromServer:
                    if val["To"]["Channel"] == toChannel and val["From"]["Channel"] == fromChannel:
                        return "{0}".format(val["Format"])#formats the message potentially
        return message #returns unformatted message if all else fails



    async def sendMessage(self,message,objDeliveryDetails,FormattingOptions,messageUnchanged): #sends the message
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)


    #work to remove this stuff eventually
    async def serviceIdentifierOld(self,fromService,fromServer,fromChannel,toService,toServer,toChannel,message): #adds a smaller easier identifier to the messages
        for key ,val in config.chatbotIdentifier.items(): #cycles through everything to eventually possibly find a match
            if val["To"]["Service"] == toService and val["From"]["Service"] == fromService:
                if val["To"]["Server"] == toServer and val["From"]["Server"] == fromServer:
                    if val["To"]["Channel"] == toChannel and val["From"]["Channel"] == fromChannel:
                        return "{0} {1}".format(val["Format"],message)#formats the message potentially
        return message #returns unformatted message if all else fails