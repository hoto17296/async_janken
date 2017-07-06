import logging
import asyncio
from message import MessageServer


class JankenServer:

    def __init__(self):
        self.clients = []
        self.logger = logging.getLogger('janken.server')
        self.server = MessageServer()
        self.server.on('connect', self.on_connect)

    def on_connect(self, connection):
        client = JankenClient(self, connection)
        self.clients.append(client)

    def on_disconnect(self, client):
        self.clients.remove(client)

    def start(self, interval=1, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            tasks = (self.server.start_async(**kwargs), self.main(interval))
            loop.run_until_complete(asyncio.wait(tasks))
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self.server.close())
            loop.close()

    async def main(self, interval):
        while True:
            await asyncio.sleep(interval)
            if len(self.clients) < 2:
                self.logger.info('waiting...')
            else:
                self.logger.info('battle!')


class JankenClient:

    def __init__(self, server, connection):
        self.server = server
        self.connection = connection
        self.id = connection.address[1]
        self.logger = logging.getLogger('janken.client[%d]' % self.id)
        self.logger.info('connected')
        connection.on('disconnect', self.on_disconnect)

    def on_disconnect(self):
        self.server.on_disconnect(self)
        self.logger.info('disconnected')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    JankenServer().start(port=8888)
