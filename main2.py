from utils.Events import Events
from utils.EventHook import EventHook
import utils
import modules
import sites
import asyncio
from sites import emotes

#this is the starting point for all the bot tasks
loop = asyncio.get_event_loop()
loop.run_forever()