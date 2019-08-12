from utils.Events import Events
from utils.EventHook import EventHook
import utils
import modules
import sites
import asyncio
from sites import emotes

#this is the starting point for all the bot tasks
discordP = sites.discord.Discord()

loop = asyncio.get_event_loop()
loop.create_task(discordP.start(utils.config.c.discordToken))
loop.run_forever()