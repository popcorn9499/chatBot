from utils.Events import Events
from utils.EventHook import EventHook
from utils import config
from sites import discord
from sites import youtube
from utils import logger
from modules import chatbot
from modules import chatLog

async def messageTest(Message):
    print(Message.Contents)




#events.onMessage += messageTest
# config.events.onMessage += messageTest

# print(config.events.__dict__)

# print(config.x)

# chatbot = chatbot.chatbot()

# chatLog = chatLog.chatLog()


# #this is the starting point for all the bot tasks
# discordP = discord.Discord()
# discordP.start(config.discordToken)




# x = input()


# if x == "1":
#     print(events.onMessage(Message="Message"))
