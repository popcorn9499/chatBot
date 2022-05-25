from sites.emotes.emotes import emotes
from sites import irc
import asyncio

class frankerfacez(emotes):
    def __init__(self):
        globalUrl = "https://api.frankerfacez.com/v1/set/global"
        channelUrlFormat = "https://api.frankerfacez.com/v1/room/" #:channel
        super().__init__(globalUrl,channelUrlFormat)
        self.services.append(irc.irc)
        asyncio.create_task(self.updateData(self.globalUrl,"global", self.parseGlobalEmoteData))
    
    async def parseGlobalEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        for val in emoteList["default_sets"]:
            emoteData = emoteList["sets"][str(val)]
            await self._getFrankerFacezEmoteSet(emoteData, emoteReturn)
        return emoteReturn

    async def _getFrankerFacesEmotesURL(self,emoteUrlList):
        emoteURL = ""
        for key,val in emoteUrlList.items():
            emoteURL = val
        return "https:" + emoteURL
    
    async def _getFrankerFacezEmoteSet(self,emote, emoteList):
        for emoticonVal in emote["emoticons"]:
            emoteUrl = await self._getFrankerFacesEmotesURL(emoticonVal["urls"])
            emoteList.update({emoticonVal["name"]: emoteUrl})

    async def parseChannelEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        for key, emoteSet in emoteList["sets"].items():
            await self._getFrankerFacezEmoteSet(emoteSet, emoteReturn)
        return emoteReturn

    async def getEmote(self,message,emojis,channel):
        await self.globalFrankerFacezEmotes(message,emojis)
        await self.channelFrankerFacezEmotes(message,emojis,channel)

    async def globalFrankerFacezEmotes(self,message,emojis):
        emoteList = self.emoteDictionary["global"]
        await self.findEmote(emoteList,message,emojis)

    async def channelFrankerFacezEmotes(self,message,emojis,channel):
        try:
            channel = channel[1:]
            channelUrL = self.channelUrlFormat + channel
            await self.checkIfEmotesCached(channel,channelUrL)
            emoteList = self.emoteDictionary[channel]
            await self.findEmote(emoteList,message,emojis)
        except: #this should theoretically just check for emotes.emotesMissing exception but this is fine as is
            pass
            

ffz = frankerfacez()