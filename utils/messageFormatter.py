import os
from utils import logger
import asyncio
from utils import fileIO

l = logger.logs("Messages")

async def formatter(unformatMsg):
    formatting = "%authorName% %message%"
    formatting = fileIO.loadConf("config{0}ChatFormatting{0}default.json")["Format"]
    for items in formatting.split(" "): #cycles through all the items and replaces the code name with the contents the message should have
        items = await removeChar("[",items)
        items = await removeChar("]",items)
        items = await removeChar(":",items)
        if items == "%message%":
            formatting = formatting.replace(items,unformatMsg.Message.Contents)
        elif items == "%roles%":
            role = await findRole(unformatMsg.FormattingOptions[items])
            formatting = formatting.replace(items,role[0])
        else:
            formatting = formatting.replace(items,unformatMsg.FormattingOptions[items])
    l.logger.info("{0}".format(formatting))
    return formatting

async def findRole(roles):
    roleName = "ehhh"
    roleNum = -666
    for roleNa,roleNu in roles.items():
        if roleNu >= roleNum:
            roleName=roleNa
            roleNum=roleNu

    return [roleName,roleNum]


async def removeChar(char,string):
    return string.replace(char,"")

