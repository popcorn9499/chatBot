from utils import tcpStream
import asyncio


class echoTest:
    def __init__(self):
        print("STarting")
        self.tcpThing = tcpStream.tcpServer("10000")
        loop = asyncio.get_event_loop()
        loop.create_task(self.start())

    async def start(self):
        msg = 2
        await asyncio.sleep(10)
        while True:
            try:
                
                if (self.tcpThing.writer != None):
                    print("sending")
                    await self.tcpThing.write(str(msg) + " hi")
                msg = msg*2
                    
            except Exception as e:
                print(e)
            await asyncio.sleep(2)

    async def readerDetails(self,output):
        print(output)
        

# e = echoTest()

