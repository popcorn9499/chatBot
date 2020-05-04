#youtube stuff imported
import httplib2

import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import time

import googleapiclient

import sys, os


from utils import config
from utils import Object
from utils import logger
from utils import messageFormatter
from utils import fileIO
import asyncio

import datetime





class Youtube:
    def __init__(self):
        self.pageToken = ""
        self.youtube = ""
        self.serviceStarted = False
        self.secretsFilePath = "config{0}auth{0}client_secrets.json".format(os.sep)
        self.oauthFilePath = "config{0}auth{0}oauth.json".format(os.sep)
        self.l = logger.logs("Youtube")
        fileIO.checkFolder("config{0}auth{0}".format(os.sep),"auth",self.l)
        fileIO.checkFile("config-example{0}auth{0}youtube.json".format(os.sep),"config{0}auth{0}youtube.json".format(os.sep),"youtube.json",self.l)
        self.enabled = fileIO.loadConf("config{0}auth{0}youtube.json")["Enabled"]
        self.pageToken = fileIO.loadConf("config{0}auth{0}youtube.json")["pageToken"]
        self.oldMessageList = [] #keeps track of old messages to filter out
        self.messageFrequency = 0
        self.isStreaming = False
        if (self.enabled):
            secretsExist = self.checkFile(self.secretsFilePath,"client_secrets.json",self.l)
            self.msgCheckList = fileIO.loadConf("config{0}auth{0}youtube.json")["selfMsgFilter"]
            if (secretsExist):
                self.l.logger.info("Starting")
                self.initAuth()
                config.events.onMessageSend += self.sendLiveChat
            else:
                self.l.logger.info("Please make sure the oauth and client secret files exist")
                #sys.exit()

    def checkFile(self,filePath,fileName,logger):
        return (os.path.isfile(filePath))

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
        self.CLIENT_SECRETS_FILE = self.secretsFilePath

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

      storage = Storage(self.oauthFilePath)
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
        self.botUserID = list_streams_request["items"][0]["snippet"]["channelId"] #saves the bots channel user id that we will use as a identifier
        self.l.logger.debug("liveID {0}".format(self.liveChatId)) #print the live chat id
        self.l.logger.debug("BotID" + str(self.botUserID))
      
     
      
    async def listChat(self):
        try:
            continuation = True
            try:
                list_chatmessages = self.youtube.liveChatMessages().list( #lists the chat messages
                    part="id,snippet,authorDetails", #gets the author details needed and the snippet all of which giving me the message and username
                    liveChatId=self.liveChatId,
                    maxResults=200,
                    pageToken=self.pageToken #gives the previous token so it loads a new section of the chat
                ).execute() #executes it so its not just some object
                self.pageToken = list_chatmessages["nextPageToken"] #page token for next use
            except googleapiclient.errors.HttpError:
                self.l.logger.info("Some Google API Error Occured")
                await self.Login()
                continuation = False 
            
            amount = 0
            if continuation == True:
                for temp in list_chatmessages["items"]: #goes through all the stuff in the list messages list
                    message = temp["snippet"]["displayMessage"] #gets the display message
                    username = temp["authorDetails"]["displayName"] #gets the users name
                    userID = temp["authorDetails"]["channelId"]
                    profilePic = temp["authorDetails"]["profileImageUrl"]
                    if message != "" and username != "": #this makes sure that the message and username slot arent empty before putting this to the discord chat        
                        self.l.logger.debug(temp)
                        fileIO.fileSave("youtubeMsgJson.json", temp)
                        self.l.logger.debug(userID)
                        self.l.logger.debug(self.botUserID)
                        if (userID != self.botUserID):#await self.weedMsg(userId,message)):
                            self.l.logger.info("{0} {1}".format(username,message))
                            await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]),profilePicture=profilePic)
                            amount = amount + 1
                        else: #check if the message was sent by the bot or not
                            msgFound = False
                            for oldMsg in self.oldMessageList:
                                if oldMsg["Message"].strip() == message.strip():
                                    msgFound = True
                            if not msgFound: #if message not sent by bot then send it
                                self.l.logger.info("{0} {1}".format(username,message))
                                await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]),profilePicture=profilePic)
                                amount = amount + 1
                            
                        # if userID != self.botUserID:
                        #     self.l.logger.info("{0} {1}".format(username,message))
                        #     await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))
                        # elif userID == self.botUserID: #if the userId is the bots then check the message to see if the bot sent it.
                        #     try:
                        #         if (message.find("[B]")==-1): #Checks the message against this to see if it was sent by the bot or a user
                        #             self.l.logger.info("{0} {1}".format(username,message))
                        #             await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))

                        #     except AttributeError as error:
                        #         self.l.logger.info("{0} {1}".format(username,message))
                        #         await self.processMsg(username=username,message=message,roleList=await self.youtubeRoles(temp["authorDetails"]))
            self.messageFrequency = amount
        except ConnectionResetError:
            x = 1
            await self.Login()
            self.l.logger.info('Connection Error reconnecting')

    async def weedMsg(self,userID,message):
        # False means its a safe message
        # true means it should be weeded out

        ##This isnt really needed anymore
        
        if userID == self.userID:
            for i in self.msgCheckList:
                if (message.find(i) == -1):
                    return False
                return True
        else:
            return False


    async def clearMsgList(self):
        oldTime = datetime.datetime.now() - datetime.timedelta(minutes=15)
        for msg in self.oldMessageList:
            if msg["Time"] < oldTime:
                self.oldMessageList.remove(msg)


    async def processMsg(self,username,message,roleList,profilePicture):
        formatOptions = {"%authorName%": username, "%channelFrom%": "Youtube", "%serverFrom%": "Youtube", "%serviceFrom%": "youtube","%message%":"message","%roles%":roleList}
        message = Object.ObjectLayout.message(Author=username,Contents=message,Server="Youtube",Channel="Youtube",Service="Youtube",Roles=roleList,profilePicture=profilePicture)
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
            return x
        except:
            await self.Login()
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
            await self.Login()
            self.l.logger.info('Connection Error reconnecting')
    
    async def getLiveStatus(self):
        try:
            x = self.youtube.liveBroadcasts().list(
            broadcastStatus="active",
            part="status",
            maxResults=50
          ).execute()
            return x
        except:
            await self.Login()
            self.l.logger.info('Connection Error reconnecting')

        

        
    async def sendLiveChat(self,sndMessage): #sends messages to youtube live chat
        while self.serviceStarted != True:
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Youtube": #determines if its the right service and supposed to be here
            msg = await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)
            time = datetime.datetime.now()
            self.oldMessageList.append({"Time":time, "Message":msg}) #keeps track of old messages so that we can check and not listen to these
            retry = 0
            while retry <= 3: #retry incase of network error. however quota likely is the issue
                try:
                    list_chatmessages_inset = self.youtube.liveChatMessages().insert(
                        part = "snippet",
                        body = dict (
                            snippet = dict(
                                liveChatId = self.liveChatId,
                                type = "textMessageEvent",
                                textMessageDetails = dict(
                                    messageText = msg
                                )
                            )
                        )
                    )  
                    list_chatmessages_inset.execute()
                    #print(list_chatmessages_inset.execute()) #debug for sending live chat messages
                except googleapiclient.errors.HttpError:
                    self.l.logger.info("Http Error Sending Msg (Likely you hit quota however will retry 3 times)")
                    retry=retry+1

            if retry > 0:
                self.l.logger.info("Http Error Sending Msg (You Hit Quota Likely")
      
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
        counter = 0
        while True:  
            if self.serviceStarted == True:  
                #try:
                await self.listChat()
                #await self.listLiveStreams()
                #await self.listLiveBroadcasts()
                await self.clearMsgList()
                if counter == 5:
                    filePath = "config{0}auth{0}youtube.json".format(os.sep)
                    data = {"Enabled": self.enabled, "pageToken": self.pageToken, "selfMsgFilter": self.msgCheckList}
                    fileIO.fileSave(filePath,data)
                    counter=0
                    self.l.logger.debug("Saving")

                    
                counter+=1
                #except googleapiclient.errors.HttpError:
                    #youtube = self.Login()
                    #self.l.logger.info('Connection Error reconnecting')
            if self.isStreaming: #check if live and determine which sleep schedule to use
                if self.messageFrequency == 0: #this should prevent overuse of the google api quota slowing down the bot during times of low use and speeding it up during times of high use
                    await asyncio.sleep(8)
                elif self.messageFrequency == 1:
                    await asyncio.sleep(5)
                elif self.messageFrequency > 1:
                    await asyncio.sleep(1)
            else:
                for i in range(0,20*60): #check every 10 seconds to see if we went live and if so leave this loop hopefully
                    if not self.isStreaming:
                        await asyncio.sleep(10)
                    else:
                        break

    async def youtubeStreamChecker(self):
        while True:
            streamData = await self.getLiveStatus()
            if len(streamData["items"]) > 0: #assume if the items in the liveStatus is above 0 then we must be streaming
                self.l.logger.info("They must be streaming now")
                self.isStreaming = True
            else:
                self.isStreaming = False
            if self.isStreaming: #when streaming check if streaming every 30 minutes
                await asyncio.sleep(30*60) 
            elif not self.isStreaming: #when not streaming check every 5 minutes
                await asyncio.sleep(5*60)
            

y = Youtube()

if (y.enabled):
    loop = asyncio.get_event_loop()
    loop.create_task(y.Login())
    loop.create_task(y.youtubeChatControl())
    loop.create_task(y.youtubeStreamChecker())
