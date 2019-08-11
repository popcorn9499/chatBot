from sites.emotes.emotes import emotes

class betterttv(enotes):
    def __init__(self):

        globalUrl = "https://api.betterttv.net/emotes"
        channelUrlFormat = "https://api.betterttv.net/2/channels/" #:channel
        super(globalUrl,channelUrlFormat)

    
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
    