import asyncio
from pyee import EventEmitter


class MessageClient(EventEmitter):

    def __init__(self, reader=None, writer=None):
        super().__init__()
        self.reader = reader
        self.writer = writer

    def connect(self, host, port):
        loop = asyncio.get_event_loop()
        try:
            future = asyncio.open_connection(host, port)
            self.reader, self.writer = loop.run_until_complete(future)
            loop.run_until_complete(self.subscribe())
        except KeyboardInterrupt:
            pass
        finally:
            self.writer.close()
            loop.close()

    def publish(self, data):
        if type(data) is str:
            data = (data+'\n').encode('utf-8')
        self.writer.write(data)

    async def subscribe(self):
        while True:
            data = await self.reader.readline()
            if data:
                print(data)
            else:
                self.emit('disconnect', self)
                return


class MessageServer(EventEmitter):

    def start(self, port):
        try:
            loop = asyncio.get_event_loop()
            future = asyncio.start_server(self.handler, port=port)
            server = loop.run_until_complete(future)
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()

    async def handler(self, reader, writer):
        client = MessageClient(reader, writer)
        self.emit('connect', client)
        return await client.subscribe()
