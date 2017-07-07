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

    async def connect(self, host, port):
        self.reader, self.writer = await asyncio.open_connection(host, port)
        self.address = self.writer.get_extra_info('peername')
        self.emit('connect')
        await self.listen()

    def send(self, event, data='\0'):
        assert(self.writer)
        assert(type(event) is str and re.compile(r'^\w*$').match(event))
        assert(type(data) is str and not re.compile(r'\n').search(data))
        message = '%s\t%s\n' % (event, data)
        self.writer.write(message.encode())

    async def listen(self):
        assert(self.reader)
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

    def close(self):
        self.writer.close()


class MessageServer(EventEmitter):

    async def start(self, **kwargs):
        self.server = await asyncio.start_server(self.handler, **kwargs)

    async def handler(self, reader, writer):
        connection = MessageConnection(reader, writer)
        self.emit('connect', connection)
        await connection.listen()

    async def close(self):
        self.server.close()
        await self.server.wait_closed()
