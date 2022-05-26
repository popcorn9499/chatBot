from utils.Events import Events
from utils.EventHook import EventHook
import utils
import modules
import sites
import asyncio
from sites import emotes
from utils import config
# #this is the starting point for all the bot tasks

    


async def run():
    config.events.onStartup() #fire off the startup event for all to view and see
    while (True):
        await asyncio.sleep(60)
        



emotes.start()


asyncio.run(run())