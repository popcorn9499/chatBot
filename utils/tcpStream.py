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

    
    async def manager(self):
        print("Starting tcp server")
        self.server = await asyncio.start_server(self.connectionHandler, self.ipAddress, self.port )
        
        async with self.server:
            await self.server.serve_forever()


    async def connectionHandler(self, reader, writer):
        self.reader = reader
        self.writer = writer
        await self.read()

    async def write(self,data):
        dataBytes = None
        if (type(data) == str):
            #dateBytes = data.encode('utf-16-le')#.strip(codecs.BOM_UTF16)
            self.writer.write(data.encode('utf-16-le'))
            
        else:
            print("data not convertable")

    async def read(self):
        print("READER")
        while True:
            # try:
            dataBytes = await self.reader.readuntil('aaaa'.encode('utf-16-le').strip(codecs.BOM_UTF16))
            
            data=dataBytes.decode('utf-16-le')
            
            await self.write(data)

            #self.writer.write(data.encode('utf-16-le'))
            if (data != ""):
                print(data)
            
            # loop = asyncio.get_event_loop()
            # loop.create_task(callback(data))
            # except ConnectionResetError:
            #     print("Connection Disconnect")
            #     break
            # except Exception as e:
            #     print("exception")
            #     print(e)
            #     pass
            await asyncio.sleep(0.01)

