from sites.emotes.emotes import emotes
from sites import irc
import asyncio

class betterttv(emotes):
    def __init__(self):
        globalUrl = "https://api.betterttv.net/emotes"
        channelUrlFormat = "https://api.betterttv.net/2/channels/" #:channel
        super().__init__(globalUrl,channelUrlFormat)
        self.services.append(irc.irc)
        self.loop.create_task(self.updateData(self.globalUrl,"global", self.parseGlobalEmoteData))

    
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
        emoteList = self.emoteDictionary["global"]
        await self.findEmote(self,emoteList,message,emojis)

    async def channelBetterttvEmotes(self,message,emojis,channel):
        channel = channel[1:]
        if not channel in self.emoteDictionary: #handle getting the data for the channel emotes if they havent been cached
            channelURL = self.channelUrlFormat + channel
            data = await self.getDataJson(channelURL)
            self.loop.create_task(self.updateData(channelURL,channel, self.parseChannelEmoteData)) #create a caching loop
            if data != None: #only update data if it got any response with data from the url
                emoteData = await self.parseChannelEmoteData(data) #parse the data into {emoteName: emoteUrl}
                self.emoteDictionary.update({channel: emoteData})
            else: #avoids a crash due to invalid channel
                return
        emoteList = self.emoteDictionary[channel]
        await self.findEmote(self,emoteList,message,emojis)
            
betterTTV = betterttv()