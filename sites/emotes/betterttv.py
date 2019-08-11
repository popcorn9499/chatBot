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

    async def getEmote(self,message,emojis,channel):
        await self.globalBetterttvEmotes(message, emojis)
        await self.channelBetterttvEmotes(message,emojis,channel)

    async def globalBetterttvEmotes(self,message,emojis):
        emoteList = super.emoteDictionary["global"]
        for key,val in emoteList.items():
            if message.find(key) != -1:
                emotes.update({key: val})

    async def channelBetterttvEmotes(self,message,emojis,channel):
        if not channel in super.emoteDictionary: #handle getting the data for the channel emotes if they havent been cached
            data = self.getDataJson()
            if data != None: #only update data if it got any response with data from the url
                emoteData = await self.parseChannelEmoteData(data) #parse the data into {emoteName: emoteUrl}
                self.emoteDictionary({channel: emoteData})
            super.loop.create_task(super.updateData(super.channel,channel, self.parseChannelEmoteData)) #create a caching loop

        emoteList = super.emoteDictionary[channel]
        for key,val in emoteList.items():
            if message.find(key) != -1:
                emotes.update({key: val})