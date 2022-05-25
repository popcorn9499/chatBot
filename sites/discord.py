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
import aiohttp
import re


#client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)

l = logger.logs("Discord")
l.logger.info("Starting")

class Discord(discord.Client):
    def __init__(self):
        super().__init__()
        fileIO.checkFolder("config{0}auth{0}".format(os.sep),"auth",l)
        fileIO.checkFile("config-example{0}auth{0}discord.json".format(os.sep),"config{0}auth{0}discord.json".format(os.sep),"discord.json",l)
        self.discordToken = fileIO.loadConf("config{0}auth{0}discord.json")["Token"]
        self.discordEnabled = fileIO.loadConf("config{0}auth{0}discord.json")["Enabled"]
        config.events.onMessageSend += self.discordSendMsg
        config.events.deleteMessage += self.delete_message
        config.events.onMessageSend += self.discordSendWebhook
        config.events.onMessageSend += self.discordSendPrivMsg
        self.discordStarted = False #shows that the discord bot has not started as of yet
        self.clientID = None #set the client id as empty until use later

    #run handler???? idk look into switching to client.run
    async def processStart(self):
        if self.discordEnabled: #allows discord to not be launched
            while True:
                try:
                    await self.start(self.discordToken,reconnect=True)
                except (discord.ConnectionClosed, discord.GatewayNotFound,discord.HTTPException,discord.ClientException) as error:
                    await self.close()
                    l.logger.info("Client Connection Lost")
                    l.logger.debug("Some error occured: " + error)
                except Exception as error: #we shall see if this fixes discord not reconnecting
                    await self.close()
                    l.logger.info("Client Connection Lost Due to unknown error...")
                    l.logger.debug("Some error occured: " + error)
                finally:
                    l.logger.info("Client Closed")
                l.logger.info("Reconnecting in 5 seconds")
                time.sleep(5)
                l.logger.info("Attempting to reconnect")
    
    async def delete_message(self,message):
        await self.delete(message)

  


    async def on_ready(self): #when the discord api has logged in and is ready then this even is fired
        l.logger.info('Logged in as')##these things could be changed a little bit here
        l.logger.info(self.user.name+ "#" + self.user.discriminator)
        botName = self.user.name+ "#" + self.user.discriminator #gets and saves the bots name and discord tag
        l.logger.info(self.user.id,)
        self.clientID = str(self.user.id)
        rolesList = {}
        membersList = {}
        discordMembers = {}
        discordRoles = {}
        for guilds in self.guilds: #this portion gets all the info for all the channels and servers the bot is in
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
            self.discordStarted = True
            l.logger.info("Started")



    async def on_message(self,message): #waits for the discord message event and pulls it somewhere
        while self.discordStarted != True:
            await asyncio.sleep(0.2)
        l.logger.debug(message.author.name + message.content)
        if str(message.author.id) != self.clientID:
            l.logger.debug(message.author.name)
            attachments = "" #gets the attachments so we dont loose that
            for i in message.attachments:
                if attachments == "":
                    attachments += i.url
                else:
                    attachments += " " + i.url 

            
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
            profilePic = message.author.avatar_url
            if (isinstance(message.channel, discord.channel.TextChannel)):
                channelName = message.channel.name
                serverName = message.guild.name
            elif (isinstance(message.channel, discord.channel.DMChannel)):
                channelName = "#{0}".format(message.author.name)
                serverName = "DM"
            elif (isinstance(message.channel, discord.channel.GroupChannel)):
                channelName = message.channel.name
                serverName = "GroupDM"
            
            #print(re.findall(r'<:\w*:\d*>', message.content))

            ######maybe use this to remove the annoying end bit of some emojis

            msgEmojis = await self.getMsgEmojis(message.content)
            l.logger.info("EMOJIS: {0}".format(msgEmojis))
            authorName = await self.getAuthor(message.author)
            messageContents = await self.userAtMentionsFix(messageContents, message.mentions)
            messageContents = await self.roleAtMentionsFix(messageContents,message.role_mentions)
            messageContents = await self.channelAtMentionsFix(messageContents,message.channel_mentions)
            formatOptions = {"%authorName%": authorName, "%channelFrom%": channelName, "%serverFrom%": serverName, "%serviceFrom%": "Discord","%message%":"message","%roles%":roleList}
            msg = Object.ObjectLayout.message(Author=authorName,User=str(message.author),Contents=messageContents,Server=serverName,Channel=channelName,Service="Discord",Roles=roleList,profilePicture=profilePic, emojis=msgEmojis)
            objDeliveryDetails = Object.ObjectLayout.DeliveryDetails(Module="Site",ModuleTo="Modules",Service="Modules",Server="Modules",Channel="Modules")
            objSendMsg = Object.ObjectLayout.sendMsgDeliveryDetails(Message=msg, DeliveryDetails=objDeliveryDetails, FormattingOptions=formatOptions,messageUnchanged=message)
            config.events.onMessage(message=objSendMsg)
            # if message.content.startswith("!hai"): #webhook testing code
            #     print(message.author.avatar_url)
            #     await Discord.webhookSend(authorName,"aa",message.channel, avatar=message.author.avatar_url)
        else:
            l.logger.debug("Why am i recieving my own messages???")


    async def getMsgEmojis(self,msg):
        msgEmojis = {}
        for emoji in self.emojis:
            print(emoji)
            if msg.find(str(emoji)) != -1:
                msgEmojis.update({str(emoji): str(emoji.url)})

        return msgEmojis

    async def getAuthor(self,user):
        try:
            if user.nick == None: #as i have found. sometimes this value isnt set for some reason and is just None. so i check for that to prevent that from causing issues
                return user.name
            else:
                return user.nick 
        except AttributeError:
            return user.name

    async def roleAtMentionsFix(self,message,mentionList):
        for role in mentionList:
            badMention = "@&" + str(role.id)
            goodMention = "@" + role.name
            message = message.replace(badMention, goodMention)
        return message

    async def channelAtMentionsFix(self,message,mentionList):
        for chanMention in mentionList:
            badMention = "#" + str(chanMention.id)
            goodMention = "#" + chanMention.name
            message = message.replace(badMention, goodMention)
        return message

    async def userAtMentionsFix(self,message,mentionList):
        for mention in mentionList:
            badMention = "@!" + str(mention.id)
            goodMention = "@" + await Discord.getAuthor(mention)
            message = message.replace(badMention, goodMention)
        return message

    async def findMember(self,username,discrim):
        while self.discordStarted != True: #wait until discord has started
            await asyncio.sleep(0.2)
        p = self.get_all_members()
        l.logger.info("NAME: {0} DISCRIM: {1}".format(username,discrim))
        member = discord.utils.get(self.get_all_members(), name=username, discriminator=str(discrim))
        l.logger.info("USER: {0}".format(member))
        return member

    async def findMemberID(self,id):
        while self.discordStarted != True: #wait until discord has started
            await asyncio.sleep(0.2)
        p = self.get_all_members()
        return discord.utils.get(p,id=int(id))


    
    async def discordSendWebhook(self,sndMessage):
        global config
        while self.discordStarted != True: #wait until discord has started
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord-Webhook": #determines if its the right service and supposed to be here
            #gather required information
            channel = self.get_channel(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel])
            embed = await self.parseEmbeds(sndMessage.customArgs)
            message = await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)
            profilePic = sndMessage.Message.ProfilePicture
            username = sndMessage.Message.Author
            #send the webhook message
            await self.webhookSend(username,message,channel,avatar=profilePic,embeds=embed)


    async def discordSendMsg(self,sndMessage): #this is for sending messages to discord
        global config
        while self.discordStarted != True:
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord": #determines if its the right service and supposed to be here
            channel = self.get_channel(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel])
            embeds = await self.parseEmbeds(sndMessage.customArgs)
            if len(embeds) != 0:
                if sndMessage.Message != None: #print the embed with a message if thats been requested.
                    await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType),embed=embeds[0])
                else: #print a messageless embed
                    await channel.send(embed=embeds[0])

                if len(embeds) > 1: #print any extra embeds that may? exist
                    for embed in embeds[1:]:
                        await channel.send(embed=embed)
            else:
                await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)) #sends the message to the channel specified in the beginning

    async def discordSendPrivMsg(self,sndMessage):
        global config
        while self.discordStarted != True:
            await asyncio.sleep(0.2)
        #l.logger.info("WHYYY {0}".format(sndMessage.DeliveryDetails.Service))
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord-Private" and sndMessage.DeliveryDetails.Server == "PrivateMessage": #determines if its the right service and supposed to be here
            if isinstance(sndMessage.DeliveryDetails.Channel, int):
                channel = await self.get_id(sndMessage.DeliveryDetails.Channel)
            elif not sndMessage.DeliveryDetails.Channel.find("#") == -1:
                discrim = int(sndMessage.DeliveryDetails.Channel[sndMessage.DeliveryDetails.Channel.rfind("#")+1:])
                username = sndMessage.DeliveryDetails.Channel[:sndMessage.DeliveryDetails.Channel.rfind("#")]
                channel = await self.findMember(username,discrim)
            l.logger.info(type(channel))
            if channel.dm_channel == None:
                await channel.create_dm()
            channel = channel.dm_channel

            embeds = await self.parseEmbeds(sndMessage.customArgs)
            if len(embeds) != 0:
                if sndMessage.Message != None: #print the embed with a message if thats been requested.
                    await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType),embed=embeds[0])
                else: #print a messageless embed
                    await channel.send(embed=embeds[0])

                if len(embeds) > 1: #print any extra embeds that may? exist
                    for embed in embeds[1:]:
                        await channel.send(embed=embed)
            else:
                await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)) #sends the message to the channel specified in the beginning

    async def parseEmbeds(self,customArgs): #cycles through any potential embeds in the message
        embeds = []
        if customArgs == None: #if never set assume no args
            return None
        for args in customArgs: #cycles through the customArgs for potential embeds
            if args["type"] == "discordEmbed":
                embeds.append(await self.discordEmbed(description=args["description"], author=args["author"], icon=args["icon"],thumbnail=args["thumbnail"],image=args["image"],fields=args["fields"],color=args["color"]))
        return embeds

    #look at this in the future to cleanup
    async def webhookSend(self,username,message, channel,avatar=None,embeds=None):
        webhooksList = await channel.webhooks()
        webhookUsed = None
        for web in webhooksList: #check if the webhook exists already in this channel
            correctName = web.name == "discordBotHook" #if not create the webhook
            correctChannel = web.channel_id == channel.id
            if correctChannel and correctName:
                webhookUsed = web
                break
        if webhookUsed == None: #if no webhook existing create one
            webhookUsed = await channel.create_webhook(name='discordBotHook')

        if embeds == None: #send webhook. check if it needs to add the embed or not
            await webhookUsed.send(message, username=username,avatar_url=avatar)
        else: 
            await webhookUsed.send(message, username=username,avatar_url=avatar,embeds=embeds)

    async def discordEmbedData(self,description=None,author=None,icon=None,thumbnail=None,image=None,fields=None,color=None):
        embedData = {"type":"discordEmbed"}
        embedData.update({"description": description})
        embedData.update({"author":author})
        embedData.update({"icon": icon})
        embedData.update({"thumbnail": thumbnail})
        embedData.update({"image":image})
        embedData.update({"fields": fields})
        embedData.update({"color":color})
        return embedData

    async def discordEmbed(self,description=None,author=None,icon=None,thumbnail=None,image=None,fields=None,color=None):
        if color ==None:
            color = discord.Colour.blue()
        if description != None:
            embed=discord.Embed(description=description, colour=color)
        else:
            embed=discord.Embed(colour=color)
        if icon != None and author != None:
            embed.set_author(name=author, icon_url=icon)
        elif author != None:
            embed.set_author(name=author)
        if thumbnail != None:
            embed.set_thumbnail(url=thumbnail)
        if image != None:
            embed.set_image(url=image)
        if not fields == None:
            for field in fields:
                if field["Name"] != "" or field["Value"] != "":
                    embed.add_field(name=field["Name"],value=field["Value"],inline=field["Inline"])
        return embed

    

discordP = Discord()

loop = asyncio.get_event_loop()
loop.create_task(discordP.processStart())

