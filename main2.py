from utils.Events import Events
from utils.EventHook import EventHook
from utils import config
from sites import discord
from utils import logger


async def messageTest(Message):
    print(Message.Contents)




#events.onMessage += messageTest
# config.events.onMessage += messageTest

# print(config.events.__dict__)

# print(config.x)




l = logger.logs("test")
l.logger.debug("test")
discordP = discord.Discord()
discordP.start(config.discordToken)




# x = input()


# if x == "1":
#     print(events.onMessage(Message="Message"))