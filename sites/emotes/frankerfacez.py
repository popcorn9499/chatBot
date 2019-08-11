from sites.emotes.emotes import emotes
import asyncio

class frankerfacez(enotes):
    def __init__(self):
        globalUrl = "https://api.frankerfacez.com/v1/set/global"
        channelUrlFormat = "https://api.frankerfacez.com/v1/room/" #:channel
        super(globalUrl,channelUrlFormat)
        super.loop.create_task(super.updateData(super.globalUrl,"global", self.parseGlobalEmoteData))

    
    async def parseGlobalEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        for val in emoteList["default_sets"]:
            for emoteData in emoteList["sets"][str(val)]:
                await self._getFrankerFacezEmoteSet(emoteData, emoteReturn)
        return emoteReturn

    async def _getFrankerFacesEmotesURL(self,emoteUrlList):
        emoteURL = ""
        for key,val in emoteUrlList.items():
            emoteURL = val
        return "https:" + emoteURL
    
    async def _getFrankerFacezEmoteSet(self,emote, emoteList):
        for emoticonVal in emote["emoticons"]:
            emoteUrl = await self.getFrankerFacesEmotesURL(emoticonVal["urls"])
            emoteList.update({emoticonVal["name"]: emoteUrl})

    async def parseChannelEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        for key, emoteSet in emoteList["sets"].items():
            await self._getFrankerFacezEmoteSet(emoteSet, emoteReturn)
        return emoteReturn