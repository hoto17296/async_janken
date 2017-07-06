import logging
import asyncio


class JankenClient:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger('janken.client')

    def connect(self, host, port):
        try:
            future = asyncio.open_connection(host, port)
            self.reader, self.writer = self.loop.run_until_complete(future)
            self.loop.run_until_complete(self.subscribe())
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

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
                print('connection closed')
                return

    def close(self):
        self.writer.close()
        self.loop.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    JankenClient().connect('localhost', 8888)
