from utils.Events import Events
from utils.EventHook import EventHook
from utils import fileIO
import os
events = Events()
x = 1




#runtime created
discordServerInfo = {}
discordRoles = {}
discord = None
discordToken = None



def loadConf(file):
    file = fileIO.fileLoad(file.format(os.sep))
    return file

discordToken = loadConf("config{0}auth{0}discord.json")["Token"]

chatbot = loadConf("config{0}chatbot{0}chatbot.json")
chatbotIdentifier = loadConf("config{0}chatbot{0}chatbotIdentifier.json")








