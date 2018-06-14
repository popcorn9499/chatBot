from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger



class chatbot:
    def __init__(self):
        self.l = logger.logs("Chatbot")
        self.l.logger.info("test")
        config.events.onMessage += self.sortMessage

    async def sortMessage(self,message):
        self.l.logger.info(message.__dict__)
        for key ,val in config.chatbot.items():
            if message.Service == val["From"]["Service"]:
                if message.Server == val["From"]["Server"]:
                    if message.Channel == val["From"]["Channel"]:
                        print("Sorted")
        pass

    async def sendMessage(self,message):
        pass