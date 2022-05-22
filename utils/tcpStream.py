import asyncio
from utils import logger
import struct
import codecs
import sys
import traceback


class tcpServer():
    def __init__(self,port):
        self.port = port
        self.ipAddress = "0.0.0.0"
        self.reader = None
        self.writer = None
        self.server = None
        loop = asyncio.get_event_loop()
        loop.create_task(self.manager())
        self.readerCallBack = []
        self.onConnectCallBack = []

    
    async def manager(self): #manages the async connection server 
        print("Starting tcp server")
        while True: #handles reloads the server
            try:
                loop = asyncio.get_event_loop()
                self.server = await asyncio.start_server(self.connectionHandler, self.ipAddress, self.port,loop=loop)
                async with self.server:
                    await self.server.serve_forever()
            except:
                self.server.close()
                pass
        

    async def readerCallBackAdder(self,callback): #allows the user to add a callback handle
        self.readerCallBack.append(callback)

    async def onConnectCallBackAdder(self,callback): #allows the user to add a callback handle
        self.onConnectCallBack.append(callback)

    async def connectionHandler(self, reader, writer): #handles connections for a single connection.    
        #this will only allow for one connection for port at this current time. may change in the future
        print("ServerStarted")
        loop = asyncio.get_event_loop()
        
        self.reader = reader
        self.writer = writer
        for callback in self.onConnectCallBack: #handles creating events for when data comes in to handle the data coming in and out
            loop.create_task(callback())
        await self.read()

    async def write(self,data):#handles writing data to the connection
        dataBytes = None
        try: #prevents any errors from crashing the task
            if (type(data) == str):
                data = data + "\r\n"
                self.writer.write(data.encode())
                print("Data Sent")
                await self.writer.drain()
            else:
                print("data not convertable")
        except ConnectionResetError:
            print("Error connection died")

    async def read(self): #reads data out of the connection asyncly
        while True: #continuously reads data out of the connection sending callbacks to the handlers to handle said data
            try:
                dataBytes = await self.reader.readuntil('\r\n'.encode()) #gets the data
                data=dataBytes.decode()
                print("DATAAA")
                if (data != ""): #prevents empty strings
                    loop = asyncio.get_event_loop()
                    data = data.replace("\r\n","")
                    print("got data")                
                    for callback in self.readerCallBack: #handles creating events for when data comes in to handle the data coming in and out
                        loop.create_task(callback(data))
            except ConnectionResetError: #handles errors on connect resets
                print("Connection Disconnect")
                break

            except asyncio.streams.IncompleteReadError: #consider too many read errors killing the connection
                pass 
            except Exception as e: #filter out any potential crashes
                print("exception")
                print(e)
                print(traceback.format_exc())
                pass
            await asyncio.sleep(0.01)

