import asyncio
from utils import logger
import struct
import codecs
import sys


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
        while True: #handles reconnects the
            try:
                self.server = await asyncio.start_server(self.connectionHandler, self.ipAddress, self.port )
            except:
                pass
        
        async with self.server:
            await self.server.serve_forever()

    async def readerCallBackAdder(self,callback):
        self.readerCallBack.append(callback)

    async def connectionHandler(self, reader, writer):
        self.reader = reader
        self.writer = writer
        await self.read()

    async def write(self,data):
        dataBytes = None
        try:
            if (type(data) == str):
                #dateBytes = data.encode('utf-16-le')#.strip(codecs.BOM_UTF16)
                self.writer.write(data.encode('utf-16-le'))
                await self.writer.drain()
            else:
                print("data not convertable")
        except ConnectionResetError:
            pass

    async def read(self): #reads data out of the connection asyncly
        print("READER")
        while True:
            try:
                dataBytes = await self.reader.readuntil('aaaa'.encode('utf-16-le').strip(codecs.BOM_UTF16)) #gets the data
                data=dataBytes.decode('utf-16-le')
                if (data != ""):                
                    loop = asyncio.get_event_loop()                
                    for callback in self.readerCallBack: #handles creating events for when data comes in to handle the data coming in and out
                        loop.create_task(callback(data))
            except ConnectionResetError: #handles errors on connect resets
                print("Connection Disconnect")
                break
            except Exception as e: #filter out any potential crashes
                print("exception")
                print(e)
                pass
            await asyncio.sleep(0.01)

