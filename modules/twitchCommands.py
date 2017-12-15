from modules import variables
from modules import mainBot


def getChannelID(self):
    from urllib.parse import urlencode
    from requests import Session
    from requests.adapters import HTTPAdapter
    from requests.exceptions import HTTPError, InvalidURL, ConnectionError
    import json
    
    clientId=variables.config["Twitch"]["clientId"]  #Register a Twitch Developer application and put its client ID here
    accessToken=variables.config["Twitch"]["accessToken"] #Generate an OAuth token with channel_subscriptions scope and insert your token here
     
    channelName= variables.config["Twitch"]["channelName"]  #Put your channel name here
    session=Session()
    channelId=""
     
     
    channelIdUrl="https://api.twitch.tv/kraken/users?login="+channelName
     
    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://',retryAdapter)
    session.mount('http://',retryAdapter)
    #Find the Channel ID
    response = session.get(channelIdUrl, headers={
    'Client-ID': clientId,
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Content-Type': 'application/json'
    })
    try:
        result = json.loads(response.text)
    except:
        result = None
    print(result)
    if (result):
        channelId = result["users"][0]["_id"]
     
    print(channelId)
    return clientId, accessToken, channelId
    
def setTitle(self,title):
    #initiate the requests library
    from urllib.parse import urlencode
    from requests import Session
    from requests.adapters import HTTPAdapter
    from requests.exceptions import HTTPError, InvalidURL, ConnectionError
    import json
    
    session=Session()
     
    clientId, accessToken, channelId =  self.getChannelID()
    
     
    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://',retryAdapter)
    session.mount('http://',retryAdapter)
    #Find the Channel ID
    result = None
    response = None
    apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId
     
    data = {"channel": {"status": title}}
    print(json.dumps(data,sort_keys=True,indent=4))
    #Do the API push data
    response = session.put(apiRequestUrl, headers={
    'Client-ID': clientId,
    'Authorization': 'OAuth '+accessToken,
    "Accept": "application/vnd.twitchtv.v5+json",
    'Content-Type': 'application/json'
    }, data=json.dumps(data,sort_keys=True,indent=4))
    try:
        result = json.loads(response.text)
    except:
        result = None
    print(result) #prints it out
    
    
def setGame(self,game):
    from urllib.parse import urlencode
    from requests import Session
    from requests.adapters import HTTPAdapter
    from requests.exceptions import HTTPError, InvalidURL, ConnectionError
    import json
    
    session=Session()
    #channelId=""
     
    clientId, accessToken, channelId =  self.getChannelID() 
     
    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://',retryAdapter)
    session.mount('http://',retryAdapter)
    #Find the Channel ID
    result = None
    response = None
     
    apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId
    
    data = {"channel": {"status": game }}
    print(data)
    #Do the API Lookup
    response = session.put(apiRequestUrl, headers={
    'Client-ID': clientId,
    'Authorization': 'OAuth '+accessToken,
    "Accept": "application/vnd.twitchtv.v5+json",
    'Content-Type': 'application/json'
    }, data=json.dumps(data,sort_keys=True,indent=4))
    try:
        result = json.loads(response.text)
    except:
        result = None
    print(result)

def getViewerCount(self):
    from urllib.parse import urlencode
    from requests import Session
    from requests.adapters import HTTPAdapter
    from requests.exceptions import HTTPError, InvalidURL, ConnectionError
    import json
    
    session=Session()
     
    clientId, accessToken, channelId =  self.getChannelID() 
     
    retryAdapter = HTTPAdapter(max_retries=2)
    session.mount('https://',retryAdapter)
    session.mount('http://',retryAdapter)
    #Find the Channel ID
    result = None
    response = None
     
    apiRequestUrl="https://api.twitch.tv/kraken/streams/"+channelId
    
    #Do the API Lookup
    response = session.get(apiRequestUrl, headers={
    'Client-ID': clientId,
    'Authorization': 'OAuth '+accessToken,
    "Accept": "application/vnd.twitchtv.v5+json",
    'Content-Type': 'application/json'
    })
    try:
        result = json.loads(response.text)
    except:
        result = None
    if result["stream"] != None:
        return result["stream"]["viewers"]
    else:
        return None