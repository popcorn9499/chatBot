import asyncio
import datetime
from utils import logger
from utils import config



class deleteService:

    def __init__(self):
        self.l = logger.logs("Delete Service")
        self.l.logger.info("Starting")
        config.events.onMessage += self.addMessage
        config.events.onMessage += self.delMessageCmd
        self.msgLibrary = []


    async def addMessage(self,message):
        time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        x = {"Message":message,"Time": time,"messageBasic":message.messageUnchanged}
        self.l.logger.debug(x)
        self.msgLibrary.append(x)
        #config.events.deleteMessage(message.messageUnchanged)

    #async findMsg

    async def delMessageCmd(self,message):
        if message.Message.Contents.startswith("!Del"):
            commandDetails = message.Message.Contents.split(" ")
            #351.20

            # command #authorToDel #Num of messages

            # command #number of messages

            # command #search delete #msg maybeee
            try:
                for i in range(len(self.msgLibrary)-int(commandDetails[1]), len(self.msgLibrary)):
                    try:
                        print(self.msgLibrary[i])
                        print(self.msgLibrary[i]["Message"].Message.Contents)
                    except IndexError:
                        pass
            except TypeError:
                pass
            self.l.logger.info("YE I GOT... I GOT IT!")




# deleteServ = deleteService()



