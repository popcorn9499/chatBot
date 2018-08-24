from utils import config
from utils import Object
import discord #gets the discord and asyncio librarys
import asyncio
import time
import datetime
from utils import logger
from utils import messageFormatter



client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)
clientID="IDK"

discordStarted = False

l = logger.logs("Discord")
l.logger.info("Starting")

class Discord:
    def __init__(self):
        pass
        config.events.onMessageSend += self.discordSendMsg
        
        


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
        for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
            for members in server.members:
                membersList.update({str(members): members})
            discordMembers.update({str(server.name):membersList})
            l.logger.debug(discordMembers)
            for roles in server.roles:
                rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
                if roles.name == "Mod":
                    pass
                    #variables.tempRole = roles
            discordRoles.update({str(server.name):rolesList})
            l.logger.debug(discordRoles)
            config.discordServerInfo.update({str(server): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
            for channel in server.channels: #get channels and add them to the list to store for later
                disc = {str(channel.name): channel}
                config.discordServerInfo[str(server)].update(disc)
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
                attachments += i["url"]
            roleList={}
            for roles in message.author.roles: #gets the authors roles and saves that to a list
                roleList.update({str(roles.name):int(roles.position)})
            l.logger.info(roleList)
            formatOptions = {"%authorName%": message.author.name, "%channelFrom%": message.channel.name, "%serverFrom%": message.server.name, "%serviceFrom%": "Discord","%message%":"message","%roles%":roleList}
            messageContents = str(message.content) + str(attachments) #merges the attachments to the message so we dont loose that.
            message = await Object.ObjectLayout.message(Author=message.author.name,Contents=messageContents,Server=message.server.name,Channel=message.channel.name,Service="Discord",Roles=roleList)
            objDeliveryDetails = await Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
            objSendMsg = await Object.ObjectLayout.sendMsgDeliveryDetails(Message=message, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions)
            config.events.onMessage(message=objSendMsg)

    async def discordSendMsg(self,sndMessage): #this is for sending messages to discord
        global config, discordInfo
        while discordStarted != True:
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord": #determines if its the right service and supposed to be here
            await client.send_message(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel], await messageFormatter.formatter(sndMessage)) #sends the message to the channel specified in the beginning

    def start(self,token):
        while True:
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(client.start(token))
            except (discord.ConnectionClosed, discord.GatewayNotFound) as error:
                loop.run_until_complete(client.logout())
                loop.close()
                start(token)
                l.logger.info("Client Connection Lost")
                # cancel all tasks lingering
            except KeyboardInterrupt:
                loop.run_until_complete(client.logout())
            finally:
                l.logger.info("Client Closed")
                loop.close()
            l.logger.info("Reconnecting")

