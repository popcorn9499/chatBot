from utils import config
from utils import Object
import asyncio
import time
import datetime
from utils import logger
from modules import messageFilter

import logging
import time
import os

print("console")

class console(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):#creates the log file with whats required
        print("Emitting")
        try:
            print("Log.log {0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message))
        except (AttributeError, UnicodeEncodeError) as e: #The unicode Error I need to find a better way to fix... 
            pass


logger.loggerHandlers.add_Logging_Handler(console())
print("Attaching console")