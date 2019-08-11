from sites.emotes.emotes import emotes
import asyncio

class frankerfacez(enotes):
    def __init__(self):
        globalUrl = "https://api.frankerfacez.com/v1/set/global"
        channelUrlFormat = "https://api.frankerfacez.com/v1/room/" #:channel
        super(globalUrl,channelUrlFormat)
        super.loop.create_task(super.updateData(super.globalUrl,"global", self.parseGlobalEmoteData))
    async def _getFrankerFacesEmotesURL(self,emoteUrlList):
        emoteURL = ""
        for key,val in emoteUrlList.items():
            emoteURL = val
        return "https:" + emoteURL
    
    async def _getFrankerFacezEmoteSet(self,emote):
        emojis = {}
        for emoticonVal in emote["emoticons"]:
            emoteUrl = await self.getFrankerFacesEmotesURL(emoticonVal["urls"])
            emojis.update({emoticonVal["name"]: emoteUrl})
        return emojis