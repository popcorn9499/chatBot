from concurrent.futures import ThreadPoolExecutor
from modules import variables
import asyncio
import time
from modules import fileIO


class mainBot():
    def main(self):
        print("bot loaded")
        cycle = 0
        #time.sleep(20)
        while True:
            if self.checkConsole() == False:
                self.checkMSG()
            self.authorMuteTimeCheck()
            if cycle == 120: 
                fileIO.fileSave("variables.config-test.json",variables.config)
                
                cycle = 0
            cycle = cycle + 1
            time.sleep(0.2)
    
    def addToConsole(self,msg,host,errorLevel):
        msgStats = {"sentFrom":"IRC","msgData": None,"Bot":"IRC","Server": host,"Channel": "Console", "author": "Console","authorData": None,"authorsRole": {"Normal": 0},"msg": msg,"Info": {"Host": host,"errorLevel": errorLevel},"sent":False}
        variables.mainMsg.append(msgStats)
        
    async def addConsoleAsync(self,msg,host,errorLevel):
        loop  = asyncio.get_event_loop()
        loop.create_task(mainBot().addConsoleAsync1(loop,msg,host,errorLevel))
        #loop.run_forever()
        
    async def addConsoleAsync1(self,loop,msg,host,errorLevel):
        await loop.run_in_executor(ThreadPoolExecutor(), self.addToConsole,msg,host,errorLevel)
        
    
    def checkConsole(self):#console sending to another service
        j = 0
        for msg in variables.mainMsg:
            try:
                if msg["Channel"] == "Console" and msg["sent"] == False:
                    
                    for key ,val in variables.config["Bot Console"].items():
                        if val["Site"] == "Terminal" and self.consoleDebugCheck(val["Debug"],msg["Info"]["errorLevel"]) == True:
                            print(self.consoleFormat(msg,val))
                        elif self.consoleDebugCheck(val["Debug"],msg["Info"]["errorLevel"]) == True:    
                            print(val)
                            fileIO.fileSave("Val",val)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":"Discord", "Server": "Popicraft Network", "Channel": "console"} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": self.consoleFormat(msg,val),"sent": False}
                            variables.processedMSG.append(msgStats)
                            print(msgStats)
                            fileIO.fileSave("console",str(msgStats))
                        
                    variables.mainMsg[j]["sent"] = True
                    return True
                    
                j = j +1
            except KeyError as error:
                print("not deleted")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
                mainBot().addToConsole('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error,"Discord"," Extra Debug")
                return False
    
    def consoleDebugCheck(self,debug,info):
        if debug[info] == True:
            return True
        else:
            return False
    
    def consoleFormat(self,msg,val):#does all console formatting
        msgStat = val["Formatting"].format(msg["Bot"],msg["Server"],msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"]),msg["Info"]["Host"],msg["Info"]["errorLevel"])
        return msgStat
    
    ##remember was working on making all the msg code the same
    def checkMSG(self):
        j = 0
        for msg in variables.mainMsg: #this cycles through the array for messages unsent to discord and sends them
            if msg["sent"] == False:
                #print(str(msg["authorData"]))
                #try: #this is here to ensure the thread doesnt crash from looking for something that doesnt exist
                if self.blacklistWorkCheck(msg,j) == False and self.commandCheck(msg,j) == False and self.authorMute(msg) == False:
                    #deleted code check
                    try:
                        if msg["deleted"] == True:
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot": msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": "[Deleted] {1} : {2}".format(msg["Bot"],msg["Server"],msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"])),"sent": False}
                            variables.processedMSG.append(msgStats)
                    except KeyError as error:
                        #print("not deleted")
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
                        mainBot().addToConsole('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error,"Discord"," Extra Debug")

                    #all channels catch portion
                    try:
                        #"*" stands for all channels
                        for key, val in variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"]["*"]["sendTo"].items(): #cycles to figure out which channels to send the message to
                            if val["Enabled"] == True and variables.config["Bot"][val["Site"]]["Enabled"] == True and variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Enabled"] == True:#this code checks to see if the message should be disabled and not sent onward
                                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":val["Site"], "Server": val["Server"], "Channel": val["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["Formatting"].format(msg["Bot"],msg["Server"],msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"])),"sent": False}
                                variables.processedMSG.append(msgStats)
                    except KeyError as error:
                        x = 1
                    try:#this is here to ensure the thread doesnt crash from looking for something that doesnt exist
                        for key, val in variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"][msg["Channel"]]["sendTo"].items(): #cycles to figure out which channels to send the message to
                            if val["Enabled"] == True and variables.config["Bot"][val["Site"]]["Enabled"] == True and variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Channel"][msg["Channel"]]["Enabled"] == True and variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Enabled"] == True:#this code checks to see if the message should be disabled and not sent onward
                                #print(msg["Bot"])
                                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":val["Site"], "Server": val["Server"], "Channel": val["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["Formatting"].format(msg["Bot"],msg["Server"],msg["Channel"],msg["author"],msg["msg"],self.botNameReformat(msg["Bot"]),self.serverNameReformat(msg["Bot"],msg["Server"]),self.channelNameReformat(msg["Bot"],msg["Server"],msg["Channel"])),"sent": False}
                                variables.processedMSG.append(msgStats)

                    except KeyError as error:
                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
                        mainBot().addToConsole('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error,"Discord"," Extra Debug")
                variables.mainMsg[j]["sent"] = True
            j = j +1
            
    def authorMuteTimeCheck(self): #this checks to see if the mute time has been up for all the muted users
        for val, key in variables.config["userMuteList"].copy().items(): #copys items to prevent it from editing a dictionary in use
            #print("{0} : {1}".format(val,key))
            
            if key["time"] == "timer":
                #gets the time checked
                variables.config["userMuteList"][val]["timeChecked"]["second"] = int(time.strftime("%S", time.gmtime()))
                variables.config["userMuteList"][val]["timeChecked"]["minute"] = int(time.strftime("%M", time.gmtime()))
                variables.config["userMuteList"][val]["timeChecked"]["hour"] = int(time.strftime("%H", time.gmtime()))
                variables.config["userMuteList"][val]["timeChecked"]["day"] = int(time.strftime("%d", time.gmtime()))
                
                #calculating the time elapsed
                variables.config["userMuteList"][val]["timeElaplsed"]["second"] = variables.config["userMuteList"][val]["timeChecked"]["second"] - int(variables.config["userMuteList"][val]["timeStarted"]["second"])
                variables.config["userMuteList"][val]["timeElaplsed"]["minute"] = variables.config["userMuteList"][val]["timeChecked"]["minute"] - int(variables.config["userMuteList"][val]["timeStarted"]["minute"])
                variables.config["userMuteList"][val]["timeElaplsed"]["hour"] = variables.config["userMuteList"][val]["timeChecked"]["hour"]- int(variables.config["userMuteList"][val]["timeStarted"]["hour"])
                variables.config["userMuteList"][val]["timeElaplsed"]["day"] = variables.config["userMuteList"][val]["timeChecked"]["day"] - int(variables.config["userMuteList"][val]["timeStarted"]["day"])
                
                #converts everything to seconds
                hour = (variables.config["userMuteList"][val]["timeElaplsed"]["day"] * 24) + variables.config["userMuteList"][val]["timeElaplsed"]["hour"]
                minute = (hour * 60) + variables.config["userMuteList"][val]["timeElaplsed"]["minute"]
                second = (minute * 60) + variables.config["userMuteList"][val]["timeElaplsed"]["second"]
                
                # calculates the time muted for to seconds
                timeMutedFor = int(key["timeMutedFor"]["minute"]) * 60
                #debug displaying
                print(second - timeMutedFor)
                print(" ")
                
                # removes user from the mute list when done
                if second >= timeMutedFor:
                    variables.config["userMuteList"].pop(val)
                    

    def authorMute(self,msg): #deletes the message when people mute others
        mute = False
        #cycles through mute list
        for val, key in variables.config["userMuteList"].items():
            #checks if the users name is muted
            if str(msg["authorData"]) == val:
                print("muted") 
                #deletes the message
                commandStats = {"sentFrom":msg["sentFrom"],"Command":"deleteMessage","args": [msg["msgData"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False} 
                variables.processedCommand.append(commandStats)
                mute = True
        print(mute)
        return mute #returns back if it was muted or not
    
    def botNameReformat(self,botName):
        if botName == "Discord":
            return "D"
        elif botName == "IRC":
            return "I"
        elif botName == "Youtube":
            return "Y"
            
            
    def serverNameReformat(self,botName,serverName):
        return variables.config["Bot"][botName]["Servers"][serverName]["showName"]
        
    def channelNameReformat(self,botName,serverName,channelName):
        return variables.config["Bot"][botName]["Servers"][serverName]["Channel"][channelName]["showName"]    
            
    def blacklistWorkCheck(self,msg,j):
        found = False
        for val in variables.config["wordBlacklist"]:#this part cycles through the actual blacklist
            for split in msg["msg"].split(): #this part cycles through every word in the message
                if split == val and found == False:#this is the check to see if the word matchs the blacklisted one and checks to see if it has already found one for said word
                    commandStats = {"sentFrom":msg["sentFrom"],"Command":"deleteMessage","args": [msg["msgData"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False} #sends delete command
                    variables.processedCommand.append(commandStats)
                    found = True #sets to true if found one blacklisted word
                    print("blacklisted")
                    variables.mainMsg[j]["sent"] = True #sets the message to true so it doesnt get cyclee through again
                    return True
        return False
                    

    def commandCheck(self,msg,j):
        realCommand = False
        commandStats = ""
        msgStats = ""
        if msg["msg"].startswith("!") == True and msg["sent"] == False:
            
            tempMsg = msg["msg"].split()
            print("MSG Type {0} {1} {2}".format(type(msg["msg"]),msg["msg"],tempMsg))
            print(variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Commands"])
            roleNum = 0
            for key,val in msg["authorsRole"].items():
                if val > roleNum:
                    roleNum = val
            print(tempMsg)
            try:
                print("before commands")
                for val in variables.config["Bot"][msg["Bot"]]["Servers"][msg["Server"]]["Commands"][tempMsg[0]]: #loops through the commands
                    print("in Commands")
                    if val["commandType"] == "setRole": #sets a role to the user
                        if  variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                            print("passed the right command and the correct role")
                            commandStats = {"sentFrom":msg["sentFrom"],"Command":"setRole","args": [val["rankToBe"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                    elif val["commandType"] == "removeRole": #removes a role from the user
                        if variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                            print("passed the right command and the correct role")
                            commandStats = {"sentFrom":msg["sentFrom"],"Command":"removeRole","args": [val["rankToBe"]],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                    elif val["commandType"] == "sendMessage": #sends a message to discord in the channel it was set to
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                    elif val["commandType"] == "setFile" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum:
                        print("placeholder")
                    elif val["commandType"] == "incrementFile" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #increments a file by blank
                        f = open(val["file"], 'r')#opens file
                        file = []
                        print("incrementFile")
                        for line in f: #pulls the file line by line into a array
                            file.append(line)
                        incrementBy = val["incrementBy"].format(int(file[val["lineToIncrement"]])).split() #splits the formatted string
                        if incrementBy[1] == "+" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #checks to see which operation needs to be  done and applys it
                            x = int(incrementBy[0]) + int(incrementBy[2])
                        elif incrementBy[1] == "-":
                            x = int(incrementBy[0]) - int(incrementBy[2])
                        elif incrementBy[1] == "*":
                            x = int(incrementBy[0]) * int(incrementBy[2])
                        elif incrementBy[1] == "/":
                            x = int(incrementBy[0]) / int(incrementBy[2])
                        elif incrementBy[1] == "//":
                            x = int(incrementBy[0]) // int(incrementBy[2])
                        elif incrementBy[1] == "**":
                            x = int(incrementBy[0]) ** int(incrementBy[2])
                        print(x)
            
                        file[val["lineToIncrement"]] = str(x) #converts it back to string and saves it to the array on said line
                        test=""
                        for x in file: #puts it back into the file
                            test = test + x
                        f.close() #closes file
                        f = open(val["file"], 'w') #writes it back to file                        
                        f.write(test)
                    elif val["commandType"] == "readFile" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #reads a file and sends it to the service
                        f = open(val["file"], 'r')#opens file
                        print("readFile")
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(f.read()),"sent": False}
                    elif val["commandType"] == "relayCommand": #will relay a command from said service (IRC,Youtube or discord)
                        print("placeholder")
                    elif val["commandType"] == "twitchSetGame" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        game = msg["msg"][len(tempMsg[0])+1:]
                        twitchBot().setGame(game)
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "twitchSetTitle" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        title = msg["msg"][len(tempMsg[0])+1:]
                        twitchBot().setGame(title)
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"]),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "twitchGetViewers" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        viewers = twitchBot().getViewerCount()
                        print("twitch viewers: " + str(viewers))
                        msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],viewers),"sent": False}
                        print("placeholder")
                    elif val["commandType"] == "userMute" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        #determining if a time was set for the mute length
                        try:
                            #gets time to set the start time of the mute to later be stored
                            startSecond = int(time.strftime("%S", time.gmtime()))
                            startMinute = int(time.strftime("%M", time.gmtime()))
                            startHour = int(time.strftime("%H", time.gmtime()))
                            startDay = int(time.strftime("%d", time.gmtime()))
                            #clears the lists of info needed
                            muteAddtimeStarted = {"second":startSecond,"minute":startMinute,"hour": startHour, "day":startDay}
                            mutedFor = {"minute": tempMsg[2]}
                            muteAdd = {"time": "timer", "timeStarted": muteAddtimeStarted,"timeChecked": muteAddtimeStarted,"timeMutedFor": mutedFor,"timeElaplsed": muteAddtimeStarted}
                            #print(muteAdd)
                            variables.config["userMuteList"].update({tempMsg[1]:muteAdd})
                            fileSave("variables.config-test.json",variables.config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1],tempMsg[2]),"sent": False}
                        except IndexError as error: #if no mute length then the mute is permenant
                            toAdd = {tempMsg[1]: {"time": "permanent"}}
                            variables.config["userMuteList"].update(toAdd)
                            fileSave("variables.config-test.json",variables.config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse1"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                    elif val["commandType"] == "userUnmute" and variables.discordRoles[msg["Server"]][val["rankRequired"]]["Number"] <= roleNum: #will relay a command from said service (IRC,Youtube or discord)
                        # !unmute (username)
                        try:
                            print("unmuted")
                            variables.config["userMuteList"].pop(tempMsg[1])
                            #print message
                            fileSave("variables.config-test.json",variables.config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                        except IndexError as error:
                            print("user not valid")
                            fileSave("variables.config-test.json",variables.config)
                            msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": val["msgResponse1"].format(msg["author"],msg["Server"],msg["Channel"],msg["Bot"],tempMsg[1]),"sent": False}
                    print("done command check")
                    if commandStats != "":
                        variables.processedCommand.append(commandStats)
                        commandStats = ""
                        return True
                    if msgStats != "":
                        variables.processedMSG.append(msgStats)
                        msgStats = ""
                        return True
                            
            except KeyError as error:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error)
                    mainBot().addToConsole('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(error).__name__, error,"Discord"," Extra Debug")
            if tempMsg[0] == "!temp" and variables.discordRoles[msg["Server"]]["Mod"]["Number"] <= roleNum:
                msgStats = {"sentFrom":msg["sentFrom"],"Bot":msg["Bot"],"Server": msg["Server"],"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"Channel":msg["Channel"], "author":msg["author"],"msg":msg["msg"],"msgFormated": "Hi user","sent": False}
                commandStats = {"sentFrom":msg["sentFrom"],"Command":"setRole","args": ["Mod"],"author":msg["author"],"authorData":msg["authorData"] ,"sendTo": {"Bot":msg["Bot"], "Server": msg["Server"], "Channel": msg["Channel"]} ,"sent": False}
                variables.processedCommand.append(commandStats)
                realCommand = True
           

            if realCommand == True:
                variables.mainMsg[j]["sent"] = True

            
            if commandStats != "":
                variables.processedCommand.append(commandStats)
               
            if msgStats != "":
                variables.processedMSG.append(msgStats)
        print("none")
        return False
