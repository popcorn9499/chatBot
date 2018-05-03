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


def loadConf():
    file = fileIO.fileLoad("config{0}auth{0}discord.json".format(os.sep))
    return file

discordToken = loadConf()["Token"]









