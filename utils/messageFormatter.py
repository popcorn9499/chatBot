async def formatter(unformatMsg):
    formatting = "%authorName% %message%"
    for items in formatting.split(" "): #cycles through all the items and replaces the code name with the contents the message should have
        print(items)
        if items == "%message%":
            string = string.replace(items,unformatMsg.Message.Contents)
        else:
            string = string.replace(items,unformatMsg.FormattingOptions[items])
    return string

