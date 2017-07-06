import re
import asyncio
from pyee import EventEmitter


class MessageConnection(EventEmitter):

    def __init__(self, reader=None, writer=None):
        super().__init__()
        self.reader = reader
        self.writer = writer
        if writer:
            self.address = writer.get_extra_info('peername')

    def connect(self, host, port):
        loop = asyncio.get_event_loop()
        try:
            future = asyncio.open_connection(host, port)
            self.reader, self.writer = loop.run_until_complete(future)
            self.address = self.writer.get_extra_info('peername')
            self.emit('connect')
            loop.run_until_complete(self.listen())
        except KeyboardInterrupt:
            self.emit('interrupt')
        finally:
            self.writer.close()
            loop.close()

    def send(self, event, data='\0'):
        assert(type(event) is str)
        assert(type(data) is str)
        message = '%s\t%s\n' % (event, data)
        self.writer.write(message.encode())

    async def listen(self):
        pattern = re.compile(r'^(.+?)\t(.*)\n')
        while True:
            message = await self.reader.readline()
            if message:
                matched = pattern.match(message.decode())
                assert(matched)
                if matched[2] != '\0':
                    self.emit(matched[1], matched[2])
                else:
                    self.emit(matched[1])
            else:
                self.emit('disconnect')
                return


class MessageServer(EventEmitter):

    def start(self, port):
        try:
            loop = asyncio.get_event_loop()
            future = asyncio.start_server(self.handler, port=port)
            server = loop.run_until_complete(future)
            loop.run_forever()
        except KeyboardInterrupt:
            self.emit('interrupt')
        finally:
            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()

    async def handler(self, reader, writer):
        connection = MessageConnection(reader, writer)
        self.emit('connect', connection)
        return await connection.listen()
