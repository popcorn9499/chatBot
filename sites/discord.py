from utils import config
from utils import Object
import discord #gets the discord and asyncio librarys
import asyncio
import time
import datetime
from utils import logger
from utils import messageFormatter
from utils import fileIO
import os


client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)
clientID="IDK"

discordStarted = False

l = logger.logs("Discord")
l.logger.info("Starting")

class Discord:
    def __init__(self):
        fileIO.checkFolder("config{0}auth{0}".format(os.sep),"auth",l)
        fileIO.checkFile("config-example{0}auth{0}discord.json".format(os.sep),"config{0}auth{0}discord.json".format(os.sep),"discord.json",l)
        config.c.discordToken = fileIO.loadConf("config{0}auth{0}discord.json")["Token"]
        config.c.discordEnabled = fileIO.loadConf("config{0}auth{0}discord.json")["Enabled"]
        config.events.onMessageSend += self.discordSendMsg
        config.events.deleteMessage += self.delete_message
   
    async def delete_message(self,message):
        await client.delete(message)


    @client.event
    async def on_ready(): #when the discord api has logged in and is ready then this even is fired
        global clientID,discordStarted
        l.logger.info('Logged in as')##these things could be changed a little bit here
        l.logger.info(client.user.name+ "#" + client.user.discriminator)
        botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
        l.logger.info(client.user.id,)
        clientID = str(client.user.id)
        rolesList = {}
        membersList = {}
        discordMembers = {}
        discordRoles = {}
        for guilds in client.guilds: #this portion gets all the info for all the channels and servers the bot is in
            for members in guilds.members:
                membersList.update({str(members): members})
            discordMembers.update({str(guilds.name):membersList})
            l.logger.debug(discordMembers)
            for roles in guilds.roles:
                rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
            discordRoles.update({str(guilds.name):rolesList})
            l.logger.debug(discordRoles)
            config.discordServerInfo.update({str(guilds): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
            for channel in guilds.channels: #get channels and add them to the list to store for later
                disc = {str(channel.name): channel.id}
                config.discordServerInfo[str(guilds)].update(disc)
            discordStarted = True
            l.logger.info("Started")


    @client.event
    async def on_message(message): #waits for the discord message event and pulls it somewhere
        while discordStarted != True:
            await asyncio.sleep(0.2)
        l.logger.debug(message.author.name + message.content)
        if str(message.author.id) != clientID:
            l.logger.debug(message.author.name)
            attachments = "" #gets the attachments so we dont loose that
            for i in message.attachments:
                attachments += i.url + " "
            messageContents = str(message.content) + str(attachments) #merges the attachments to the message so we dont loose that.
            roleList={}
            try: 
                for roles in message.author.roles: #gets the authors roles and saves that to a list
                    roleList.update({str(roles.name):int(roles.position)})
            except AttributeError:
                l.logger.info("{0}: {1} ".format(message.author.name,messageContents))
            l.logger.info(roleList)
            #await client.delete_message(message)
            channelName = ""
            serverName = ""
            authorName = ""
            profilePic = message.author.avatar_url
            if (isinstance(message.channel, discord.channel.TextChannel)):
                channelName = message.channel.name
                serverName = message.guild.name
                if message.author.nick != None:
                    authorName = message.author.nick
                else:
                    authorName = message.author.name
            elif (isinstance(message.channel, discord.channel.DMChannel)):
                channelName = "#{0}".format(message.author.name)
                serverName = "DM"
                authorName =message.author.name
            elif (isinstance(message.channel, discord.channel.GroupChannel)):
                channelName = message.channel.name
                serverName = "GroupDM"
                authorName =message.author.name

            formatOptions = {"%authorName%": authorName, "%channelFrom%": channelName, "%serverFrom%": serverName, "%serviceFrom%": "Discord","%message%":"message","%roles%":roleList}
            msg = Object.ObjectLayout.message(Author=authorName,User=str(message.author),Contents=messageContents,Server=serverName,Channel=channelName,Service="Discord",Roles=roleList,profilePicture=profilePic)
            objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
            objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=msg, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged=message)
            config.events.onMessage(message=objSendMsg)
        else:
            l.logger.debug("Why am i recieving my own messages???")


    async def discordSendMsg(self,sndMessage): #this is for sending messages to discord
        global config
        while discordStarted != True:
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord": #determines if its the right service and supposed to be here
            channel = client.get_channel(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel])
            await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)) #sends the message to the channel specified in the beginning
            
    def start(self,token):
        if config.c.discordEnabled: #allows discord to not be launched
            while True:
                loop = asyncio.get_event_loop()
                try:
                    loop.run_until_complete(client.start(token,reconnect=True))
                except (discord.ConnectionClosed, discord.GatewayNotFound,discord.HTTPException,discord.ClientException) as error:
                    loop.run_until_complete(client.logout())
                    loop.close()
                    start(token)
                    l.logger.info("Client Connection Lost")
                    l.logger.debug("Some error occured: " + error)
                    # cancel all tasks lingering
                except KeyboardInterrupt:
                    loop.run_until_complete(client.logout())
                finally:
                    l.logger.info("Client Closed")
                    loop.close()
                l.logger.info("Reconnecting")

