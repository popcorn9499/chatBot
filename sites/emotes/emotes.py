from utils import config

import json

import aiohttp
import asyncio


class emotes():
    def __init__(self,globalUrl=None,channelUrl=None):
        self.globalUrl = globalUrl
        self.channelUrlFormat = channelUrl
        self.channelUrl = {} #{Channel: channelName, URL: url}
        self.updateDelay = 5*60
        self.emoteDictionary = {}
        self.services=[] #list of services allowed to be subscribed to this emote
        self.loop = asyncio.get_event_loop()
        config.events.subscribeEmoteEngine += self.subscribeEmote
    
    async def subscribeEmote(self,service,emoteHandleList):
        for checkService in self.services:
            if isinstance(service, checkService):
                emoteHandleList.append(self)

    async def getEmote(self,message,emojis,channel):
        #emojis should add to a dictionary in the format of {emoteName: emoteURL}
        pass

    async def getDataJson(self,url):
        emoteList = None
        async with aiohttp.ClientSession(json_serialize=json.dump) as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                emoteList = await resp.json()
 
        return emoteList



    async def updateData(self, url, dictionaryTag, dataParser):
        while True:
            data = await self.getDataJson(url)
            if data != None: #only update data if it got any response with data from the url
                emoteData = await dataParser(data) #parse the data into {emoteName: emoteUrl}
                self.emoteDictionary.update({dictionaryTag: emoteData})
            await asyncio.sleep(self.updateDelay)

    async def findEmote(self,emoteList,message,emojis):
        for key,val in emoteList.items():
            if message.find(key) != -1:
                emojis.update({key: val})

    async def checkIfEmotesCached(self,channel,channelURL):
        if not channel in self.emoteDictionary: #handle getting the data for the channel emotes if they havent been cached
            data = await self.getDataJson(channelURL)
            self.loop.create_task(self.updateData(channelURL,channel, self.parseChannelEmoteData)) #create a caching loop
            if data != None: #only update data if it got any response with data from the url
                emoteData = await self.parseChannelEmoteData(data) #parse the data into {emoteName: emoteUrl}
                self.emoteDictionary.update({channel: emoteData})
            else: #avoids a crash due to invalid channel
                raise emotesMissing()

class emotesMissing(Exception):
    pass
