import logging
import time
from utils import config
import os

class loggerHandlers:
    def __init__(self):
        #config.events.newLogger += self.add
        self.loggerInstances = []
        self.loggerHandlers = []

    def add(self,logger):
        logger.info("Adding logging handler" )
        print(self.loggerHandlers)
        self.loggerInstances.append(logger)
        for handlers in self.loggerHandlers:
            self._add_handler(handlers,logger)

    def add_Logging_Handler(self,handler):
        self.loggerHandlers.append(handler)
        print("Adding handler to loggers")
        print(self.loggerHandlers)
        print(self.loggerInstances)
        for logger in self.loggerInstances:
            self._add_handler(handler,logger)

    def _add_handler(self,handler,loggerInst):
        loggerInst.addHandler(handler)


class logs:
    def __init__(self,name): #creates the logger object
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s [Thread/%(threadName)s] - %(name)s - %(levelname)s - %(message)s') #sets formatting for the console output
        terminal = logging.StreamHandler()
        terminal.setLevel(logging.INFO)#sets the debug level
        terminal.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(terminal) #adds the console handlerth
        self.logger.addHandler(LogFile())#adds the log file handler
        loggerHandlers.add(self.logger)



class LogFile(logging.Handler):
    def emit(self, record):#creates the log file with whats required
        try:
            self.logFile("Log.log","{0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message))
        except (AttributeError, UnicodeEncodeError) as e: #The unicode Error I need to find a better way to fix... 
            pass

    def logFile(self,file,msg): #creates the file with what was specified to be put into it
        current_time = time.time()
        #potential for rotating logs or something
        # if os.path.isfile(file) and library.creationTime(current_time,file) >= (3600*24):
        #         os.rename(file, file + ".1")
        with open(file, 'a') as f:#'a' allows us to append a new line to the file
            f.write(msg + "\r\n") #writes the line to the file


loggerHandlers = loggerHandlers()