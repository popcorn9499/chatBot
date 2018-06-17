class Object():
    def __init__(self, attributes:dict):
        self.__dict__ = attributes


class ObjectLayout:

    async def message(Contents,Author,Server,Channel,Service,Roles):
        messageObj = Object({"Contents":Contents,"Author":Author,"Server":Server,"Channel":Channel,"Service":Service,"Roles":Roles})
        #print(messageObj.__dict__)
        return messageObj
    
    async def DeliveryDetails(Module,ModuleTo,Service,Server,Channel):
        DeliveryDetailsObj = Object({"Module":Module,"ModuleTo":ModuleTo,"Service": Service,"Server": Server, "Channel": Channel})
        return DeliveryDetailsObj

    async def sendMsgDeliveryDetails(Message,DeliveryDetails):
        sendMsgDeliveryDetails = Object({"Message": Message, "DeliveryDetails":DeliveryDetails})
        return sendMsgDeliveryDetails
        

# #me playing around code
# t = Object({"test":1,"why":5})
# print(t.why)


#things I will need to layout
#this was mostly gotten off a look at the discord py documenation

'''
Messages:
-timestamp
-edited_timestamp?
-tts?
-type?
-author #this would give the member or user information depending on variables
-content
-embeds
-server

-mentions_everyone?




Roles: #ranks etc
-id
-name
-permissions
-server
-position
-managed?
-mentionable
-created_at
-mention?


-Roles: #option
-list all roles and in which order


Server:
-name
-emojis
-members
-channels
-icon
-id
-owner
-unavaliable? #basically would stop the bot from doing anything if the server cant be used
-large? #probably unnessisary
-default_channel
-created_at
-role hierarchy
-get_channel
-get_member




Channel:
-name
-id
-server
-topic
-is_private
-position
-type: voice or text private or group or category
-is_default?
-created_at



Member:? 

User:
-name
-id
-discrimitantor
-avatar
-bot #bool if its bot or not
-mention
-display_name




Private Channel:?

'''