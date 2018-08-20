import os
from utils import fileIO



async def formatter(unformatMsg):
    formatting = "%authorName% %message%"
    formatting = fileIO.loadConf("config{0}ChatFormatting{0}default.json")["Format"]
    for items in formatting.split(" "): #cycles through all the items and replaces the code name with the contents the message should have
        items = await removeChar("[",items)
        items = await removeChar("]",items)
        items = await removeChar(":",items)
        if items == "%message%":
            formatting = formatting.replace(items,unformatMsg.Message.Contents)
        else:
            formatting = formatting.replace(items,unformatMsg.FormattingOptions[items])
    return formatting

async def removeChar(char,string):
    return string.replace(char,"")

