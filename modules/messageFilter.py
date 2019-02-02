from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger
from utils import fileIO
import os

class messageFilter:
    def __init__(self):
        self.l = logger.logs("messageFilter")
        fileIO.checkFolder("config{0}messageFilter{0}".format(os.sep),"messageFilter",self.l)
        fileIO.checkFile("config-example{0}messageFilter{0}config.json".format(os.sep),"config{0}messageFilter{0}config.json".format(os.sep),"config.json",self.l)
        self.filter = fileIO.loadConf("config{0}messageFilter{0}config.json")["Message Filter"]
        pass

    async def filterMessage(self,message):
        contents = message.Contents
        for i in self.filter:
            if (contents.find(i) != -1):
                #should send a log potentially if config setup for that
                #should also probably delete the message from the previous service as well as not let it through. whatever is calling this
                return True
        return False

    


messageFilter = messageFilter()