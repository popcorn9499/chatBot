from sites.emotes.emotes import emotes
import asyncio

class betterttv(enotes):
    def __init__(self):

        globalUrl = "https://api.betterttv.net/emotes"
        channelUrlFormat = "https://api.betterttv.net/2/channels/" #:channel
        super(globalUrl,channelUrlFormat)
        super.loop.create_task(super.updateData(super.globalUrl,"global", self.parseGlobalEmoteData))

    
    async def parseGlobalEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        for emoteData in emoteList["emotes"]:
            emoteName = emoteData["regex"]
            emoteUrl = "https:" + emoteData["url"]
            emoteUrl = emoteUrl.replace("/1x", "/3x")
            emoteReturn.update({emoteName: emoteUrl})
        return emoteReturn

    async def parseChannelEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        emoteUrlTemplate = "https:" + emoteList["urlTemplate"] #gets a template url
        for emoteData in emoteList["emotes"]:
            emoteName = emoteData["code"]
            emoteUrl =  emoteUrlTemplate.replace("{{id}}", emoteData["id"])
            emoteUrl = emoteUrl.replace("{{image}}", "/3x")
            emoteReturn.update({emoteName: emoteUrl})
        return emoteReturn

    async def getEmote():
        pass
    
    async def betterttvEmotes(self,message,emojis,channel):
        await self.globalBetterttvEmotes(message, emojis)
        await self.channelBetterttvEmotes(message,emojis,channel)

    async def globalBetterttvEmotes(self,message,emojis):
        emoteList = super.emoteDictionary["global"]
        for key,val in emoteList.items():
            if message.find(key) != -1:
                emotes.update({key: val})

    async def channelBetterttvEmotes(self,message,emojis,channel):
        emoteUrl = "" + channel

        emoteList = json.loads(requestData.content)
        emoteUrlTemplate = "https:" + emoteList["urlTemplate"]
        if emoteList["status"] != 200 or "message" in emoteList:
            return None
        emoteList = emoteList["emotes"]
        for emoteData in emoteList:
            if message.find(emoteData["code"]) != -1:
                emoteUrl =  emoteUrlTemplate.replace("{{id}}", emoteData["id"])
                emoteUrl = emoteUrl.replace("{{image}}", "/3x")
                emojis.update({emoteData["code"]: emoteUrl})