#youtube stuff imported
import httplib2

import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import time

from modules import variables
from modules import mainBot
from modules import fileIO
import sys, os


youtube = ""







# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please variables.configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Retrieve a list of the liveStream resources associated with the currently
# authenticated user's channel.

def getLiveId(youtube): #this gets the live chat id
    global liveChatId,botUserID #pulls in the bots livechatid and botuserid for further saving and modifying
  
    list_streams_request = youtube.liveBroadcasts().list( #checks for the live chat id through this
        part="snippet", #this is what we look through to get the live chat id
        broadcastStatus="all", #we need both of these to get the live chat id
        broadcastType="all"
    ).execute() #executes it so its not just some object
    liveChatId = list_streams_request["items"][0]["snippet"]["liveChatId"]#sifts through the output to get the live chat id and saves it
    botUserID = list_streams_request["items"][1]["snippet"]["channelId"] #saves the bots channel user id that we will use as a identifier
    print("liveID {0}".format(liveChatId)) #print the live chat id
    #print("BotID" + str(botUserID))
  
 
  
def listChat():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global youtube
    try:
        continuation = True
        try:
            list_chatmessages = youtube.liveChatMessages().list( #lists the chat messages
                part="id,snippet,authorDetails", #gets the author details needed and the snippet all of which giving me the message and username
                liveChatId=liveChatId,
                maxResults=500,
                pageToken=variables.config["Bot"]["Youtube"]["pageToken"] #gives the previous token so it loads a new section of the chat
            ).execute() #executes it so its not just some object
            variables.config["Bot"]["Youtube"]["pageToken"] = list_chatmessages["nextPageToken"] #page token for next use
        except googleapiclient.errors.HttpError:
            continuation = False 
            
        msgCheckRegex = re.compile(r'(:)') #setup for if we happen to need this it should never change either way
        if continuation == True:
            for temp in list_chatmessages["items"]: #goes through all the stuff in the list messages list
                message = temp["snippet"]["displayMessage"] #gets the display message
                username = temp["authorDetails"]["displayName"] #gets the users name
                userID = temp["authorDetails"]["channelId"]
                if message != "" and username != "": #this makes sure that the message and username slot arent empty before putting this to the discord chat        
                    print(temp)
                    fileIO.fileSave("youtubeMsgJson.json", temp)
                    print(userID)
                    print(botUserID)
                    if userID != botUserID:
                        print("{0} {1}".format(username,message))
                        msgStats = {"sentFrom":"Youtube","msgData": None,"Bot":"Youtube","Server": "None","Channel": variables.config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorsRole": youtubeRoles(temp["authorDetails"]),"msg":message,"sent":False}
                        variables.mainMsg.append(msgStats)
                    elif userID == botUserID: #if the userId is the bots then check the message to see if the bot sent it.
                        try:
                            msgCheckComplete = msgCheckRegex.search(message) #checks the message against the previously created regex for ":"
                            if msgCheckComplete.group(1) != ":": #if its this then go and send the message as normal
                                print("{0} {1}".format(username,message))
                                msgStats = {"sentFrom":"Youtube","msgData": None,"Bot":"Youtube","Server": "None","Channel": variables.config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorRole": youtubeRoles(temp["authorDetails"]),"msg":message,"sent":False}
                                variables.mainMsg.append(msgStats)
                        except AttributeError as error:
                            print("{0} {1}".format(username,message))
                            msgStats = {"sentFrom":"Youtube","msgData": None,"Bot":"Youtube","Server": "None","Channel": variables.config["Bot"]["Youtube"]["ChannelName"], "author": username,"authorData":None,"authorsRole": youtubeRoles(temp["authorDetails"]),"msg":message,"sent":False}
                            variables.mainMsg.append(msgStats)    
    except ConnectionResetError:
        x = 1
        mainBot.mainBot().addToConsole('Connection Error reconnecting',"Youtube","Info")
        youtube = Login()
        
    


def youtubeRoles(authorDetails):
    roles = {}
    if authorDetails["isChatModerator"] == True:
        roles.update({"Mod":2})
    if authorDetails["isChatOwner"] == True:
        roles.update({"Owner":3})
    if authorDetails["isChatSponsor"] == True:
        roles.update({"Sponsor":1})
    roles.update({"Normal": 0})
    print("roles {0}".format(roles))
    return roles 
    
def listLiveStreams():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global youtube           
    x = list_streams_request = youtube.liveStreams().list(
        part="id,snippet",
        mine=True,
        maxResults=50
    ).execute()
    fileIO.fileSave("youtubeliveStreamsJson.json", x)
    
    
def listLiveBroadcasts():
    global pageToken #pulls in the page token
    global liveChatId #pulls in the liveChatID
    global botUserID #pulls in the bots channel ID
    global youtube       
    x = youtube.liveBroadcasts().list(
    broadcastStatus="all",
    part="id,snippet",
    maxResults=50
  ).execute()
    fileIO.fileSave("youtubeliveBroadcastsJson.json", x)    

    

    
def sendLiveChat(msg): #sends messages to youtube live chat
    list_chatmessages_inset = youtube.liveChatMessages().insert(
        part = "snippet",
        body = dict (
            snippet = dict(
                liveChatId = liveChatId,
                type = "textMessageEvent",
                textMessageDetails = dict(
                    messageText = msg
                )
            )
        )
    )  
    list_chatmessages_inset.execute()
    #print(list_chatmessages_inset.execute()) #debug for sending live chat messages
  
def Login():
    if "__main__" == "__main__":
        args = argparser.parse_args()
            
        youtube = get_authenticated_service(args) #authenticates the api and saves it to youtube
        getLiveId(youtube)   
        return youtube
    
def youtubeChatControl():
    while True:    
        listChat()
        listLiveStreams()
        listLiveBroadcasts()
        j = 0
        for msg in variables.processedMSG: #this cycles through the array for messages unsent to irc and sends them
            if msg["sent"] == False and msg["sendTo"]["Bot"] == "Youtube":
                sendLiveChat(msg["msgFormated"])#sends the message to the irc from whatever
                variables.processedMSG[j]["sent"] = True
            j = j + 1
        time.sleep(2) 


youtube = Login()
print("logged in to youtube")