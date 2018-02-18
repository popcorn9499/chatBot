from utils.EventHook import EventHook
class Events(object):
    def __init__(self):
        Event = EventHook()
        self.onMessage = EventHook()
        self.onConnect = EventHook()
        self.onMessageDelete = EventHook()
        self.onMessageEdit = EventHook()
        self.onReactAdd = EventHook()
        self.onReactRemove = EventHook()
        self.onReady = EventHook()
        self.onMemberJoin = EventHook()
        self.onMemberUpdate = EventHook()





# events = Events()

# events.on_message += messageTest("test")



# '''
# -On Connect #Creates the connection


# -On Message #spews message object

# -On Ready #Spews ready information

# -On Error #spews error

# -On Message Delete

# -On Message Edit

# -On React Add

# -On React Remove

# -On Channel Delete

# -On Channel Create

# -On Channel Update

# -On Member Join

# -On Member Update

# -On Server Join

# -On Server Remove

# -On Server Update

# -On Server Role Create

# -On Server Role Delete

# -On Server Role Update

# -On Server Emojis Update

# -On Server Avaliable

# -On Server Unavaliable

# -On Member Ban

# -On Member Unban

# -On Typing?

# -On Group Join?

# -On Group Remove?
# '''