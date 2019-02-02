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
        pass

    async def filterMessage


messageFilter = messageFilter()