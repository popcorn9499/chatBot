from utils import config
from utils import Object
import discord #gets the discord and asyncio librarys
import asyncio
import time
import datetime
from utils import logger
client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)


l = logger.logs("Discord")
l.logger.debug("test")

@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    l.logger.info('Logged in as')##these things could be changed a little bit here
    l.logger.info(client.user.name+ "#" + client.user.discriminator)
    botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
    l.logger.info(client.user.id,)


    rolesList = {}
    membersList = {}
    discordMembers = {}
    discordRoles = {}
    for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
        for members in server.members:
            membersList.update({str(members): members})
        discordMembers.update({str(server.name):membersList})
        l.logger.warning(discordMembers)
        for roles in server.roles:
            #print( "[" + server.name + "]"+ roles.name + ":" + str(roles.position))
            rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
            if roles.name == "Mod":
                pass
                #variables.tempRole = roles

        discordRoles.update({str(server.name):rolesList})
        l.logger.warning(discordRoles)


        config.discordServerInfo.update({str(server): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
        for channel in server.channels: #get channels and add them to the list to store for later
            disc = {str(channel.name): channel}
            config.discordServerInfo[str(server)].update(disc)


@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    #print(message.author.name + message.content)
    attachments = "" #gets the attachments so we dont loose that
    for i in message.attachments:
        attachments += i["url"]
        
    roleList={}
    for roles in message.author.roles: #gets the authors roles and saves that to a list
        roleList.update({str(roles.name):int(roles.position)})
    messageContents = str(message.content) + str(attachments) #merges the attachments to the message so we dont loose that.
    obj = await Object.ObjectLayout.message(Author=message.author.name,Contents=messageContents,Server=message.server.name,Channel=message.channel.name,Service="Discord",Roles=roleList)
    config.events.onMessage(obj)

async def discordSendMsg(msg): #this is for sending messages to discord
    global config, discordInfo
    await client.send_message(discordInfo[msg["Server"]][msg["ChannelTo"]], msg["msgFormated"]["Discord"]) #sends the message to the channel specified in the beginning
    


def start(token):
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(token))
    except (discord.ConnectionClosed, discord.GatewayNotFound) as error:
        loop.run_until_complete(client.logout())
        loop.close()
        start(token)
        # cancel all tasks lingering
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()