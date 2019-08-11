
import json

import requests #replace this sometime in the future
import asyncio


class emotes():
    def __init__(self,url,channelUrl=None):
        self.url = url
    
    
    async def getDataJson(self,url):
        requestData = requests.get()
        if requestData.status_code != 200:
            return None
        emoteList = json.loads(requestData.content)
        if emoteList["status"] != 200:
            return None
        return emoteList