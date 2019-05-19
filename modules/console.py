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
        try:
            loop  = asyncio.get_event_loop() #this should handle taking a sync task and converting it to async more or less..
            loop.create_task(self.sendMessage("Log.log {0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message)))
        except (AttributeError, UnicodeEncodeError) as e: #The unicode Error I need to find a better way to fix... 
            pass

    async def sendMessage(self,message): #sends the message
        formatType = "MutedOther"
        formattingSettings = "%message%"
        FormattingOptions = {"%message%":"message"}
        message = Object.ObjectLayout.message(Author="Console",Contents=message,Server="Popicraft Network",Channel="console-test",Service="Discord",Roles={})
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Console",ModuleTo="Site",Service="Discord", Server="Popicraft Network",Channel="console-test") #prepares the delivery location
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)
        
     

logger.loggerHandlers.add_Logging_Handler(console())
print("Attaching console")