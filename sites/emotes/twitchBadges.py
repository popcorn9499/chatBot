from sites.emotes.emotes import emotes
from sites import irc
import asyncio

class twitchBadges(emotes):
    def __init__(self):
        globalUrl = "https://badges.twitch.tv/v1/badges/global/display?language=en"
        channelUrlFormat = "https://badges.twitch.tv/v1/badges/channels/{0}/display?language=en" #:channel
        super().__init__(globalUrl,channelUrlFormat)
        self.services.append(irc.irc)
        self.loop.create_task(self.updateData(self.globalUrl,"global", self.parseGlobalEmoteData))

    
    async def parseGlobalEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        #emote url here is the different badge versions
        for emoteData in emoteList["badge_sets"]:
            versionsData = await self.getAllVersions(emoteList["badge_sets"][emoteData]["versions"])
            emoteName = emoteData
            emoteReturn.update({emoteName: versionsData})
        return emoteReturn

    async def parseChannelEmoteData(self,emoteList):
        emoteReturn = {} #this should be in {emoteName: emoteUrl} format
        #emote url here is the different badge versions
        for emoteData in emoteList["badge_sets"]:
            versionsData = await self.getAllVersions(emoteList["badge_sets"][emoteData]["versions"])
            emoteName = emoteData
            emoteReturn.update({emoteName: versionsData})
        return emoteReturn

    async def getAllVersions(self,data): #pass it "versions"
        versionsData = {} #"version#": "URL"
        for x in data:
            version = data[x]
            versionsData.update({x: version["image_url_4x"]})
        return versionsData

    async def getEmote(self,message,emojis,channel):
        pass

    # async def globalBetterttvEmotes(self,message,emojis):
    #     emoteList = self.emoteDictionary["global"]
    #     await self.findEmote(emoteList,message,emojis)

    # async def channelBetterttvEmotes(self,message,emojis,channel): 
    #     #channel should be room-id
    #     try:
    #         channelUrL = self.channelUrlFormat.format(channel)
    #         await self.checkIfEmotesCached(channel,channelUrL)
    #         emoteList = self.emoteDictionary[channel]
    #         await self.findEmote(emoteList,message,emojis)
    #     except: #this should theoretically just check for emotes.emotesMissing exception but this is fine as is
    #         pass


    async def getBadges(self,badge,badgeVersion,badges,channel):
        #channel should be room id
        #Global handling
        try:
            badgeUrl = await self.findBadge(self.emoteDictionary["global"],badge,badgeVersion)
            badges.update({badge: badgeUrl})
        except noBadge:
            pass
        #channel handling. 
        try:
            channelUrL = self.channelUrlFormat.format(channel)
            await self.checkIfEmotesCached(channel,channelUrL)
            emoteList = self.emoteDictionary[channel]
            badgeUrl = await self.findBadge(emoteList,badge,badgeVersion)
            badges.update({badge: badgeUrl})
        except: #this should theoretically just check for emotes.emotesMissing exception but this is fine as is
            pass


    async def findBadge(self,badgeList,badge,realBadgeVersion):
        badgeVersions = badgeList[badge]
        badgeVer = -1
        for badgeVersion in badgeVersions:
            if realBadgeVersion == badgeVersion:
                badgeVer = badgeVersion
        if badgeVer == -1:
            raise noBadge()
        badgeUrl = badgeVersions[badgeVer]
        return badgeUrl

TwitchBadges = twitchBadges()


class noBadge(Exception):
    pass