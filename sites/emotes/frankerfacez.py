
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