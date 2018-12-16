#youtube stuff imported
import httplib2

import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import time

from utils import fileIO
import sys, os


from utils import config
from utils import Object
from utils import logger
from utils import messageFormatter
import asyncio





class Youtube:
    def __init__(self):
        self.pageToken = ""
        self.youtube = ""
        self.serviceStarted = False
        self.l = logger.logs("Youtube")
        self.l.logger.info("Starting")
        self.initAuth()
        self.msgCheckRegex = re.compile(r'(:)') #setup for if we happen to need this it should never change either way
        config.events.onMessageSend += self.sendLiveChat

    def initAuth(self):
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
        self.CLIENT_SECRETS_FILE = "client_secrets.json"

        # This OAuth 2.0 access scope allows for full read/write access to the
        # authenticated user's account.
        self.YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please variables.configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

           %s

        with information from the {{ Cloud Console }}
        {{ https://cloud.google.com/console }}

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           self.CLIENT_SECRETS_FILE))

    async def get_authenticated_service(self,args):
      flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
        scope=self.YOUTUBE_READ_WRITE_SCOPE,
        message=self.MISSING_CLIENT_SECRETS_MESSAGE)

      storage = Storage("%s-oauth2.json" % sys.argv[0])
      credentials = storage.get()

      if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

      return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

    # Retrieve a list of the liveStream resources associated with the currently
    # authenticated user's channel.

    async def getLiveId(self): #this gets the live chat id
      
        list_streams_request = self.youtube.liveBroadcasts().list( #checks for the live chat id through this
            part="snippet", #this is what we look through to get the live chat id
            broadcastStatus="all", #we need both of these to get the live chat id
            broadcastType="all"
        ).execute() #executes it so its not just some object
        self.liveChatId = list_streams_request["items"][0]["snippet"]["liveChatId"]#sifts through the output to get the live chat id and saves it
        self.botUserID = list_streams_request["items"][1]["snippet"]["channelId"] #saves the bots channel user id that we will use as a identifier
        self.l.logger.info("liveID {0}".format(self.liveChatId)) #print the live chat id
        self.l.logger.info("BotID" + str(self.botUserID))
      
     
      
    async def listChat(self):
        try:
            continuation = True
            try:
                list_chatmessages = self.youtube.liveChatMessages().list( #lists the chat messages
                    part="id,snippet,authorDetails", #gets the author details needed and the snippet all of which giving me the message and username
                    liveChatId=self.liveChatId,
                    maxResults=500,
                    pageToken=self.pageToken #gives the previous token so it loads a new section of the chat
                ).execute() #executes it so its not just some object
                self.pageToken = list_chatmessages["nextPageToken"] #page token for next use
            except googleapiclient.errors.HttpError:
                continuation = False 
                
            
            if continuation == True:
                for temp in list_chatmessages["items"]: #goes through all the stuff in the list messages list
                    message = temp["snippet"]["displayMessage"] #gets the display message
                    username = temp["authorDetails"]["displayName"] #gets the users name
                    userID = temp["authorDetails"]["channelId"]
                    if message != "" and username != "": #this makes sure that the message and username slot arent empty before putting this to the discord chat        
                        self.l.logger.debug(temp)
                        fileIO.fileSave("youtubeMsgJson.json", temp)
                        self.l.logger.debug(userID)
                        self.l.logger.debug(self.botUserID)
                        if userID != self.botUserID:
                            self.l.logger.info("{0} {1}".format(username,message))
                            await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))
                        elif userID == self.botUserID: #if the userId is the bots then check the message to see if the bot sent it.
                            try:
                                msgCheckComplete = self.msgCheckRegex.search(message) #checks the message against the previously created regex for ":"
                                if msgCheckComplete.group(1) != ":": #if its this then go and send the message as normal
                                    self.l.logger.info("{0} {1}".format(username,message))
                                    await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))

                            except AttributeError as error:
                                self.l.logger.info("{0} {1}".format(username,message))
                                await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))
        except ConnectionResetError:
            x = 1
            youtube = await self.Login()
            self.l.logger.info('Connection Error reconnecting')
            
    async def processMsg(self,username,message,roleList):
        formatOptions = {"%authorName%": username, "%channelFrom%": "Youtube", "%serverFrom%": "Youtube", "%serviceFrom%": "youtube","%message%":"message","%roles%":roleList}
        message = Object.ObjectLayout.message(Author=username,Contents=message,Server="Youtube",Channel="Youtube",Service="Youtube",Roles=roleList)
        objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
        objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged="None")
        config.events.onMessage(message=objSendMsg)


    async def youtubeRoles(self,authorDetails):
        roles = {}
        if authorDetails["isChatModerator"] == True:
            roles.update({"Mod":2})
        if authorDetails["isChatOwner"] == True:
            roles.update({"Owner":3})
        if authorDetails["isChatSponsor"] == True:
            roles.update({"Sponsor":1})
        roles.update({"Normal": 0})
        self.l.logger.debug("roles {0}".format(roles))
        return roles 
        
    async def listLiveStreams(self):       
        try:
            x = list_streams_request = self.youtube.liveStreams().list(
                part="id,snippet",
                mine=True,
                maxResults=50
            ).execute()
            fileIO.fileSave("youtubeliveStreamsJson.json", x)
        except:
            youtube = await self.Login()
            self.l.logger.info('Connection Error reconnecting')
        
        
    async def listLiveBroadcasts(self):
        try:
            x = self.youtube.liveBroadcasts().list(
            broadcastStatus="all",
            part="id,snippet",
            maxResults=50
          ).execute()
            fileIO.fileSave("youtubeliveBroadcastsJson.json", x)
        except:
            youtube = await self.Login()
            self.l.logger.info('Connection Error reconnecting')

        

        
    async def sendLiveChat(self,sndMessage): #sends messages to youtube live chat

        while self.serviceStarted != True:
            await asyncio.sleep(5)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Youtube": #determines if its the right service and supposed to be here
            list_chatmessages_inset = self.youtube.liveChatMessages().insert(
                part = "snippet",
                body = dict (
                    snippet = dict(
                        liveChatId = self.liveChatId,
                        type = "textMessageEvent",
                        textMessageDetails = dict(
                            messageText = await messageFormatter.formatter(sndMessage)
                        )
                    )
                )
            )  
            #list_chatmessages_inset.execute()
            print(list_chatmessages_inset.execute()) #debug for sending live chat messages
      
    async def Login(self):

        if "__main__" == "__main__":
            self.l.logger.info("Logging In")
            args = argparser.parse_args()
            
            self.youtube = await self.get_authenticated_service(args) #authenticates the api and saves it to youtube
            await self.getLiveId() 
            self.l.logger.info("Logged in")
            self.serviceStarted = True
        
    async def youtubeChatControl(self):
        self.l.logger.info("Started")
        while True:  
            if self.serviceStarted == True:  
                #try:
                await self.listChat()
                await self.listLiveStreams()
                await self.listLiveBroadcasts()
                #except googleapiclient.errors.HttpError:
                    #youtube = self.Login()
                    #self.l.logger.info('Connection Error reconnecting')
            await asyncio.sleep(2)


y = Youtube()


loop = asyncio.get_event_loop()
loop.create_task(y.Login())
loop.create_task(y.youtubeChatControl())
