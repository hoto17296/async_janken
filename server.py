import logging
from message import MessageServer

class Env:

    def __init__(self):
        self.clients = []
        self.logger = logging.getLogger('janken.env')

    def on_connect(self, client):
        self.clients.append(client)
        self.logger.info('connected')
        client.on('disconnect', self.on_disconnect)

    def on_disconnect(self):
        self.logger.info('disconnected')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    server = MessageServer()
    server.on('connect', Env().on_connect)
    server.start(port=8888)
