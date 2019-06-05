import asyncio
from utils import logger
import struct
import codecs
import sys
import traceback


class tcpServer():
    def __init__(self,port):
        self.port = port
        self.ipAddress = "localhost"
        self.reader = None
        self.writer = None
        self.server = None
        loop = asyncio.get_event_loop()
        loop.create_task(self.manager())
        self.readerCallBack = []

    
    async def manager(self): #manages the async connection server 
        print("Starting tcp server")
        while True: #handles reloads the server
            try:
                self.server = await asyncio.start_server(self.connectionHandler, self.ipAddress, self.port )
                async with self.server:
                    await self.server.serve_forever()
            except:
                self.server.close()
                pass
        

    async def readerCallBackAdder(self,callback): #allows the user to add a callback handle
        self.readerCallBack.append(callback)

    async def readerCallbackRemover(self,callback):
        self.readerCallBack.remove(callback)

    async def connectionHandler(self, reader, writer): #handles connections for a single connection.    
        #this will only allow for one connection for port at this current time. may change in the future
        self.reader = reader
        self.writer = writer
        await self.read()

    async def write(self,data):#handles writing data to the connection
        dataBytes = None
        try: #prevents any errors from crashing the task
            if (type(data) == str):
                self.writer.write(data.encode('utf-16-le').strip(codecs.BOM_UTF16))
                await self.writer.drain()
            else:
                print("data not convertable")
        except ConnectionResetError:
            pass

    async def read(self): #reads data out of the connection asyncly
        while True: #continuously reads data out of the connection sending callbacks to the handlers to handle said data
            try:
                dataBytes = await self.reader.readuntil('weDone'.encode('utf-16-le').strip(codecs.BOM_UTF16)) #gets the data
                data=dataBytes.decode('utf-16-le')
                if (data != ""): #prevents empty strings
                    loop = asyncio.get_event_loop()                
                    for callback in self.readerCallBack: #handles creating events for when data comes in to handle the data coming in and out
                        loop.create_task(callback(data))
            except ConnectionResetError: #handles errors on connect resets
                print("Connection Disconnect")
                break
            except Exception as e: #filter out any potential crashes
                print("exception")
                print(e)
                print(traceback.format_exc())
                pass
            await asyncio.sleep(0.01)

