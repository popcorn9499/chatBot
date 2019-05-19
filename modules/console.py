from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger
from modules import messageFilter

import logging
import time
import os

print("console")

class console(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):#creates the log file with whats required
        print("Emitting")
        try:
            loop  = asyncio.get_event_loop()

            loop.create_task(self.sendMessage("Log.log {0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message)))
        except (AttributeError, UnicodeEncodeError) as e: #The unicode Error I need to find a better way to fix... 
            pass

    async def sendMessage(self,message): #sends the message
        
        formatType = "MutedOther"
        formattingSettings = "%message%"
        FormattingOptions = {"%message%":"message"}
        message = Object.ObjectLayout.message(Author="Console",Contents=message,Server="Popicraft Network",Channel="console-test",Service="Discord",Roles={})
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Console",ModuleTo="Site",Service="Discord", Server="Popicraft Network",Channel="console-test") #prepares the delivery location
        # ServiceIcon = await self.serviceIdentifier(fromService=msg.Service,fromServer=msg.Server,fromChannel=msg.Channel,toService=val["To"]["Service"],toServer=val["To"]["Server"],toChannel=val["To"]["Channel"],message=msg.Contents) #sees if it needs to be identified
        # formatOptions.update({"%serviceIcon%": ServiceIcon}) #Adds more formatting options
        #,objDeliveryDetails,FormattingOptions,formattingSettings,formatType,messageUnchanged
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)
        
     

logger.loggerHandlers.add_Logging_Handler(console())
print("Attaching console")