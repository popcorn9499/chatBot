from utils import config

import json

import requests #replace this sometime in the future
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
        requestData = requests.get(url)
        if requestData.status_code != 200:
            return None
        emoteList = json.loads(requestData.content)
        if emoteList["status"] != 200:
            return None
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