from utils import config

import discord #gets the discord and asyncio librarys
import asyncio
import time
import datetime

client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)




@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    print('Logged in as',"Discord","Info")##these things could be changed a little bit here
    print(client.user.name+ "#" + client.user.discriminator,"Discord","Info")
    botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
    print(client.user.id,"Discord","Info")


    rolesList = {}
    membersList = {}
    for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
        for members in server.members:
            membersList.update({str(members): members})
        config.discordMembers.update({str(server.name):membersList})
        print(config.discordMembers,"Discord","Extra Debug")
        for roles in server.roles:
            #print( "[" + server.name + "]"+ roles.name + ":" + str(roles.position))
            rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
            if roles.name == "Mod":
                pass
                #variables.tempRole = roles

        config.discordRoles.update({str(server.name):rolesList})
        print(config.discordRoles,"Discord","Extra Debug")


        config.discordServerInfo.update({str(server): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
        for channel in server.channels: #get channels and add them to the list to store for later
            disc = {str(channel.name): channel}
            config.discordServerInfo[str(server)].update(disc)


@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    print(message.author.name + message.content)
    config.events.onMessage(message.author.name + message.content)

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