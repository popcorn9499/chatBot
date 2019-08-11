
import json

import requests #replace this sometime in the future
import asyncio


class emotes():
    def __init__(self,globalUrl=None,channelUrl=None):
        self.globalUrl = globalUrl
        self.channelUrlFormat = channelUrl
        self.channelUrl = {} #{Channel: channelName, List: listData, URL: url, Timeout: time}
        self.updateDelay = 5*60
    
    
    async def getDataJson(self,url):
        requestData = requests.get()
        if requestData.status_code != 200:
            return None
        emoteList = json.loads(requestData.content)
        if emoteList["status"] != 200:
            return None
        return emoteList

    async def updateData(self, parameter_list):
        while True:

            await asyncio.sleep()