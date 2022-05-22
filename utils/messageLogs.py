import datetime

class messageLogs:

    def __init__(self):
        self.l = logger.logs("Message Log Service")
        self.l.logger.info("Starting")
        config.events.onMessage += self.addMessage
        config.messageLogs = self
        self.msgLibrary = []

    async def addMessage(self,message):
        time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        x = {"Message":message,"Time": time,"messageBasic":message.messageUnchanged}
        self.l.logger.debug(x)
        self.msgLibrary.append(x)

    async def findMsg(message,author,channel,server,service):
        for messageLog in self.msgLibrary:
            isAuthor = messageLog.message.Message.Author == author
            isChannel = messageLog.message.Message.Channel == channel
            isServer = messageLog.message.Message.Server == server
            isServer = messageLog.message.Message.Service == service
            isMessage = False #Figure out how i would like to layout this. 
            '''
                figure out how to handle messages. maybe... say... find to see if it exists at all...
                potentially add another event or function for onLog or something to keep track of *sent* messages
            '''
            #if
            return False 

