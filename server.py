import logging
import asyncio


class JankenServerClient:

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.logger = logging.getLogger('janken.server.client')

    def publish(self, data):
        if type(data) is str:
            data = (data+'\n').encode('utf-8')
        self.writer.write(data)

    async def subscribe(self):
        self.publish('foo!')
        while True:
            data = await self.reader.readline()
            if data:
                print(data)
            else:
                self.logger.info('connection closed')
                return

    def close(self):
        pass
        # TODO remove from client list


class JankenServer:

    def __init__(self):
        self.clients = []
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger('janken.server')

    def start(self, port):
        try:
            future = asyncio.start_server(self.handler, port=port)
            self.server = self.loop.run_until_complete(future)
            self.loop.call_soon(self.battle)
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

    async def handler(self, reader, writer):
        client = JankenServerClient(reader, writer)
        self.clients.append(client)
        return await client.subscribe()

    def battle(self, interval=1):
        # TODO Battle
        self.loop.call_later(interval, self.battle)

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    JankenServer().start(port=8888)
