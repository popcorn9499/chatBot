from utils.Events import Events
from utils.EventHook import EventHook
from utils import fileIO
events = Events()
x = 1

class config():
    def __init__(self):
        pass


#runtime created
discordServerInfo = {}
discordRoles = {}
discord = None
discordToken = None




c = config()



chatLogRules = fileIO.loadConf("config{0}chatLog{0}logRules.json")








