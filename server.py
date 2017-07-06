import logging
import asyncio
from message import MessageServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('janken.server')


class Env:

    def __init__(self):
        self.clients = []

    def on_connect(self, connection):
        client = Client(connection)
        self.clients.append(client)

    async def start(self, interval):
        while True:
            await asyncio.sleep(interval)
            if len(self.clients) < 2:
                logger.info('waiting...')
            else:
                logger.info('battle!')


class Client:

    def __init__(self, connection):
        self.connection = connection
        self.id = connection.address[1]
        self.logger = logging.getLogger('janken.client[%d]' % self.id)
        self.logger.info('connected')
        connection.on('disconnect', self.on_disconnect)

    def on_disconnect(self):
        self.logger.info('disconnected')


if __name__ == '__main__':
    server = MessageServer()
    env = Env()
    server.on('connect', env.on_connect)
    try:
        loop = asyncio.get_event_loop()
        tasks = (server.start_async(port=8888), env.start(1))
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(server.close())
        loop.close()
