from utils.Events import Events
from utils.EventHook import EventHook
from utils import config
from sites import discord
from sites import youtube
from sites import irc
from utils import logger
from utils import deleteMsg
# from modules import console #move the location of this please... it must start closer to the beginning....
# from modules import chatbot
# from modules import chatLog
# from modules import command


import modules


async def messageTest(Message):
    print(Message.Contents)




#events.onMessage += messageTest
# config.events.onMessage += messageTest

# print(config.events.__dict__)

# print(config.x)





#this is the starting point for all the bot tasks
discordP = discord.Discord()
discordP.start(config.c.discordToken)




# x = input()


# if x == "1":
#     print(events.onMessage(Message="Message"))
