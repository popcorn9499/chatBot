from utils.Events import Events
from utils.EventHook import EventHook
import utils
import modules
import sites
from sites import emotes

#this is the starting point for all the bot tasks
discordP = sites.discord.Discord()
discordP.start(utils.config.c.discordToken)

