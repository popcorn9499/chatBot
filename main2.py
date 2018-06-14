from utils.Events import Events
from utils.EventHook import EventHook
from utils import config
from sites import discord
from utils import logger
from modules import chatbot

async def messageTest(Message):
    print(Message.Contents)




#events.onMessage += messageTest
# config.events.onMessage += messageTest

# print(config.events.__dict__)

# print(config.x)

chat = chatbot.chatbot()

discordP = discord.Discord()
discordP.start(config.discordToken)




# x = input()


# if x == "1":
#     print(events.onMessage(Message="Message"))
