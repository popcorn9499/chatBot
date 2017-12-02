from modules import mainBot
from modules import variables
from modules import fileIO
import discord #gets the discord and asyncio librarys
import asyncio
import time
import datetime


firstRun = "off"
discordInfo = {}
haltDiscordMSG = 0
haltDeleteMSG = 0 

client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)


async def discordSendMsg(msg): #this is for sending messages to discord
    global config, discordInfo
    await client.send_message(discordInfo[msg["Server"]][msg["ChannelTo"]], msg["msgFormated"]["Discord"]) #sends the message to the channel specified in the beginning
    
async def discordCheckMsg(): #checks for a discord message
    global haltDiscordMSG, haltDeleteMSG, config
    j = 0
    for msg in variables.processedMSG: #this cycles through the array for messages unsent to discord and sends them
        if msg["sent"] == False and msg["sendTo"]["Bot"] == "Discord": 
            #await discordSendMsg(msg) #sends message
            await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            variables.processedMSG[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1
        
        
async def discordCheckCommand(): #checks for a discord message
    global haltDiscordMSG, haltDeleteMSG, config,discord
    j = 0
    for command in variables.processedCommand: #this cycles through the array for messages unsent to discord and sends them
        if command["sent"] == False: 
            if command["Command"] == "setRole":
                await mainBot.mainBot().addConsoleAsync('Setting role',"Discord","Extra Info")
                await client.add_roles(command["authorData"], variables.discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif command["Command"] == "removeRole":
                await mainBot.mainBot().addConsoleAsync('Removing role',"Discord","Extra Info")
                await client.remove_roles(command["authorData"], variables.discordRoles["Popicraft Minecraft"][command["args"][0]]["Data"])
            elif  command["Command"] == "sendMessage":
                await mainBot.mainBot().addConsoleAsync('PlaceHolder for Send message',"Discord","Extra Info")
            elif command["Command"] == "deleteMessage":
                await mainBot.mainBot().addConsoleAsync('Deleted message',"Discord"," Extra Info")
                await client.delete_message(command["args"][0])
            
            
            
                
            #await client.send_message(discordInfo[msg["sendTo"]["Server"]][msg["sendTo"]["Channel"]], msg["msgFormated"]) #sends the message to the channel specified in the beginning
            variables.processedCommand[j]["sent"] = True#promptly after sets that to the delete code
        j = j + 1

@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    global ircClient,firstRun
    firstRun = "off"
    if firstRun == "off":
        #print(discord.Server)
        #these 2 variables are used to keep track of what channel is thre real channel to use when sending messages to discord
        global config , botName, discordMSG,discordInfo, haltDiscordMSG,haltDeleteMSG
        global channelToUse #this is where we save the channel information (i think its a class)
        global  channelUsed #this is the channel name we are looking for
        #this is just to show what the name of the bot is and the id
        await mainBot.mainBot().addConsoleAsync('Logged in as',"Discord","Info")##these things could be changed a little bit here
        await mainBot.mainBot().addConsoleAsync(client.user.name+ "#" + client.user.discriminator,"Discord","Info")
        botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
        await mainBot.mainBot().addConsoleAsync(client.user.id,"Discord","Info")
        rolesList = {}
        membersList = {}
        for server in client.servers: #this portion gets all the info for all the channels and servers the bot is in
            for members in server.members:
                membersList.update({str(members): members})
            variables.discordMembers.update({str(server.name):membersList})
            await mainBot.mainBot().addConsoleAsync(variables.discordMembers,"Discord","Extra Debug")
            for roles in server.roles:
                #print( "[" + server.name + "]"+ roles.name + ":" + str(roles.position))
                rolesList.update({str(roles.name):{"Number":int(roles.position),"Data": roles}})
                if roles.name == "Mod":
                    variables.tempRole = roles
            variables.discordRoles.update({str(server.name):rolesList})
            await mainBot.mainBot().addConsoleAsync(variables.discordRoles,"Discord","Extra Debug")
            discordInfo.update({str(server): {"asdasdhskajhdkjashdlk":"channel info"}})#maybe set a check for that channel
            for channel in server.channels:
                disc = {str(channel.name): channel}
                discordInfo[str(server)].update(disc)
        while True:
            if haltDiscordMSG == 0:
                haltDeleteMSG = 1
                await discordCheckMsg()
                await discordCheckCommand()
                await asyncio.sleep(1)
            
    else:
        await getFirstRunInfo()
                
       
#I need to get the person who deleted this message to make this useful            
# @client.event
# async def on_message_delete(message): #waits for the discord message event and pulls it somewhere
    # global variables.mainMsg,discord,variables.tempRole,variables.discordRoles,variables.processedCommand
    # if firstRun == "off":
        # if str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            # print("[Deleted]{0} : {1}".format(message.author,message.content)) #prints this to the screen
            # # await client.send_message(message.channel, 'Hello.')          
            # # ircSendMSG(message.author,config["ircChannel"],message.content)
            # roleList = {}
            # for roles in message.author.roles:
                # print(roles.name + ":" + str(roles.position))
                # roleList.update({str(roles.name):int(roles.position)})
            # print(roleList)
            # print(variables.tempRole)
            # # commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            # # variables.processedCommand.append(commandStats)
            # # await client.add_roles(message.author, variables.discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            # msgStats = {"sentFrom":"Discord","deleted": True,"msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":message.content,"sent":False}
            # variables.mainMsg.append(msgStats)
    
@client.event
async def on_error(event):
    #print("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    f = open("error.log","r+")
    f.write("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event))
    await mainBot.mainBot().addConsoleAsync("[{0:%Y-%m-%d %H:%M:%S}][ERROR] {1}".format(datetime.datetime.now(),event),"Discord","Debug")
    f.close()
    
    
@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    if firstRun == "off":
        if str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            #print("{0} : {1}".format(message.author,message.content)) #prints this to the screen
            #await client.send_message(message.channel, 'Hello.')          
            #ircSendMSG(message.author,config["ircChannel"],message.content)
            roleList = {}
            attachments = ""
            for i in message.attachments:
                attachments += i.url
            for roles in message.author.roles:
                #await mainBot.mainBot().addConsoleAsync(roles.name + ":" + str(roles.position),"Discord","Info") #causes a weird bot:14 spam in console every message
                roleList.update({str(roles.name):int(roles.position)})
            print(roleList)
            print(variables.tempRole)
            #commandStats = {"Command":"deleteMessage","args": [message],"sent": False}
            #variables.processedCommand.append(commandStats)
            #await client.add_roles(message.author, variables.discordRoles["Popicraft Minecraft"]["Mod"]["Data"])
            messageContent = str(message.content) + str(attachments)
            await mainBot.mainBot().addConsoleAsync("{0} : {1}".format(message.author,messageContent),"Discord","Info")
            msgStats = {"sentFrom":"Discord","msgData": message,"Bot":"Discord","Server": str(message.server.name),"Channel":str(message.channel.name), "author":message.author.name,"authorData":message.author,"authorsRole":roleList,"msg":messageContent,"sent":False}
            variables.mainMsg.append(msgStats)

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