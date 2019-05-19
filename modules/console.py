#this module is intended to give a console to your bot when it loads. 
#It may miss some early boot process stuff as it loads a little later in the boot process

from utils import config
from utils import Object
from utils import fileIO
import asyncio
import time
import datetime
from utils import logger
from modules import messageFilter

import logging
import time
import os




class console(logging.Handler):
    def __init__(self):
        self.l = logger.logs("Console")
        fileIO.checkFolder("config{0}console{0}".format(os.sep),"console",self.l)
        fileIO.checkFile("config-example{0}console{0}console.json".format(os.sep),"config{0}console{0}console.json".format(os.sep),"console.json",self.l)
        file = fileIO.loadConf("config{0}console{0}console.json")

        self.consoleOutputs = file["Consoles"]


        super().__init__()

    def emit(self, record):#creates the log file with whats required
        try:
            loop  = asyncio.get_event_loop() #this should handle taking a sync task and converting it to async more or less..
            loop.create_task(self.cycleConsoles("Log.log {0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message)))
            print("done")
        except (AttributeError, UnicodeEncodeError) as e: #The unicode Error I need to find a better way to fix... 
            pass

    async def cycleConsoles(self,message):
        for console in self.consoleOutputs:
            message = Object.ObjectLayout.message(Author="Console",Contents=message,Server=console["Server"],Channel=console["Channel"],Service=console["Service"],Roles={})
            objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Console",ModuleTo="Site",Service=console["Service"], Server=console["Server"],Channel=console["Channel"]) #prepares the delivery location
            formattingSettings = console["Formatting"]
            await self.sendMessage(message,objDeliveryDetails,formattingSettings)


    async def sendMessage(self,message,objDeliveryDetails,formattingSettings): #sends the message
        formatType = "MutedOther"
        FormattingOptions = {"%message%":"message"}
        
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails,FormattingOptions=FormattingOptions,formattingSettings=formattingSettings,formatType=formatType,messageUnchanged=message) #prepares the delivery object and sends the message send event
        config.events.onMessageSend(sndMessage=objSendMsg)
        
     

logger.loggerHandlers.add_Logging_Handler(console())
print("Attaching console")