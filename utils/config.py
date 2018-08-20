from utils.Events import Events
from utils.EventHook import EventHook
from utils import fileIO
events = Events()
x = 1




#runtime created
discordServerInfo = {}
discordRoles = {}
discord = None
discordToken = None





discordToken = fileIO.loadConf("config{0}auth{0}discord.json")["Token"]

chatbot = fileIO.loadConf("config{0}chatbot{0}chatbot.json")
chatbotIdentifier = fileIO.loadConf("config{0}chatbot{0}chatbotIdentifier.json")


chatLogRules = fileIO.loadConf("config{0}chatLog{0}logRules.json")








