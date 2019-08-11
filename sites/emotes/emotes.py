
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
            data = self.getDataJson(url)
            if data != None: #only update data if it got any response with data from the url
                emoteData = await dataParser(data) #parse the data into {emoteName: emoteUrl}
                self.emoteDictionary({dictionaryTag: emoteData})
            await asyncio.sleep(self.updateDelay)