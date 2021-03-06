import os
from utils import logger
import asyncio
from utils import fileIO

l = logger.logs("Messages")

async def formatter(unformatMsg,formattingOptions="default.json",formatType="File"):
    return await _formatter(unformatMsg.Message.Contents, unformatMsg.FormattingOptions,formattingOptions,formatType)
    
async def _formatter(message,formattingOptionsItems,formattingOptions="default.json",formatType="File"):   
    if (formatType == "File"):
        formatting = fileIO.loadConf("config{0}ChatFormatting{0}"+formattingOptions)["Format"]
    elif (formatType == "Other") or (formatType == "MutedOther"):
        formatting = formattingOptions
    if formattingOptions == None:
        return None
    for items in formatting.split(" "): #cycles through all the items and replaces the code name with the contents the message should have
        items = await removeChar("[",items)
        items = await removeChar("]",items)
        items = await removeChar(":",items)
        try:
            if items == "%message%":
                formatting = formatting.replace(items,message)
            elif items == "%roles%":
                role = await findRole(formattingOptionsItems[items])
                formatting = formatting.replace(items,role[0])
            else:
                formatting = formatting.replace(items,formattingOptionsItems[items])
        except KeyError: #prevents format stryings that dont exist from crashing the formatter
            pass
    if (formatType != "MutedOther"):
        l.logger.info("{0}".format(formatting))
    return formatting

async def checkMessage(string):
        output = ""
        for x in string:
            try:
                x.encode('cp1252')
                output = output+x
            except:
                pass
        print(output)
        return output

async def findRole(roles):
    roleName = ""
    roleNum = -666
    for roleNa,roleNu in roles.items():
        if roleNu >= roleNum:
            roleName=roleNa
            roleNum=roleNu

    return [roleName,roleNum]


async def removeChar(char,string):
    return string.replace(char,"")

