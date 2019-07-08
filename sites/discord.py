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
        config.events.onWebhookSend += self.discordSendWebhook
   
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
                try:
                    if message.author.nick != None:
                        authorName = message.author.nick
                    else:
                        authorName = message.author.name
                except AttributeError: #is handled cuz webhooks dont have a nick only a name
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
            if message.content.startswith("!hai"):
                print(message.author.avatar_url)
                await Discord.webhookSend(authorName,"aa",message.channel, avatar=message.author.avatar_url)
        else:
            l.logger.debug("Why am i recieving my own messages???")

    async def discordSendWebhook(self,sndMessage):
        global config
        while discordStarted != True: #wait until discord has started
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord": #determines if its the right service and supposed to be here
            #gather required information
            channel = client.get_channel(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel])
            embed = await Discord.parseEmbeds(sndMessage.customArgs)
            message = await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)
            profilePic = sndMessage.Message.ProfilePicture
            username = sndMessage.Message.Author
            #send the webhook message
            await Discord.webhookSend(username,message,channel,avatar=profilePic,embeds=embed)


    async def discordSendMsg(self,sndMessage): #this is for sending messages to discord
        global config
        while discordStarted != True:
            await asyncio.sleep(0.2)
        if sndMessage.DeliveryDetails.ModuleTo == "Site" and sndMessage.DeliveryDetails.Service == "Discord": #determines if its the right service and supposed to be here
            channel = client.get_channel(config.discordServerInfo[sndMessage.DeliveryDetails.Server][sndMessage.DeliveryDetails.Channel])
            embeds = await Discord.parseEmbeds(sndMessage.customArgs)
            if embeds != None:
                if sndMessage.Message != None: #print the embed with a message if thats been requested.
                    await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType),embed=embeds[0])
                else: #print a messageless embed
                    await channel.send(embed=embeds[0])

                if len(embeds) > 1: #print any extra embeds that may? exist
                    for embed in embeds[1:]:
                        await channel.send(embed=embed)
            else:
                await channel.send(await messageFormatter.formatter(sndMessage,formattingOptions=sndMessage.formattingSettings,formatType=sndMessage.formatType)) #sends the message to the channel specified in the beginning


    async def parseEmbeds(customArgs): #cycles through any potential embeds in the message
        embeds = []
        if customArgs == None: #if never set assume no args
            return None
        for args in customArgs: #cycles through the customArgs for potential embeds
            if args["type"] == "discordEmbed":
                embeds.append(await Discord.discordEmbed(description=args["description"], author=args["author"], icon=args["icon"],thumbnail=args["thumbnail"],image=args["image"],fields=args["fields"],color=args["color"]))
        return emebds

    async def webhookSend(username,message, channel,avatar=None,embeds=None):
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

    async def discordEmbedData(description=None,author=None,icon=None,thumbnail=None,image=None,fields=None,color=None):
        embedData = {"type":"discordEmbed"}
        embedData.update({"description": description})
        embedData.update({"author":author})
        embedData.update({"icon": icon})
        embedData.update({"thumbnail": thumbnail})
        embedData.update({"image":image})
        embedData.update({"fields": fields})
        embedData.update({"color":color})
        return embedData

    async def discordEmbed(description=None,author=None,icon=None,thumbnail=None,image=None,fields=None,color=None):
        if description != None:
            embed=discord.Embed(description=description, colour=color)
        else:
            embed=discord.Embed(colour=discord.Colour.blue())
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
                embed.add_field(name=field["Name"],value=field["Value"],inline=field["Inline"])
        return embed

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

