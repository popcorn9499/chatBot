import logging
import time
import os

class logs:
    def __init__(self,name):
        print("ya?")
        self.logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s [Thread/%(threadName)s] - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.addHandler(LogFile())


class LogFile(logging.Handler):
    def emit(self, record):
        print("ran")
        print(record.__dict__)
        self.logFile("Log.log","{0} [Thread/{1}] - {2} - {3} - {4} ".format(record.asctime,record.threadName,record.name,record.levelname,record.message))

    def logFile(self,file,msg):
        current_time = time.time()

        if os.path.isfile(file) and library.creationTime(current_time,file) >= (3600*24): 
                os.rename(file, file + ".1")
        with open(file, 'a') as f:
            f.write(msg + "\r\n")

