import logging
import asyncio
import json
import numpy as np
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

    async def start(self, interval=1, **kwargs):
        await self.server.start(**kwargs)
        await self.main(interval)

    async def main(self, interval):
        counter = 1
        while True:
            await asyncio.sleep(interval)
            if len(self.clients) < 2:
                self.logger.info('waiting...')
            else:
                self.logger.info('battle:%d' % counter)
                self.battle = JankenBattle(self, self.clients.copy())
                message = json.dumps({ 'n': len(self.clients) })
                self.broadcast('ready', message)
                counter += 1

    def judge(self, results):
        for client, action, judge in results:
            action_str = ['✋', '✌', '✊'][action-1]
            judge_str = ['Lose...', 'Draw', 'Win!'][int(judge)+1]
            self.logger.info('%s %s %s' % (client.id, action_str, judge_str))
            client.send('judge', str(judge))


    def broadcast(self, *args):
        for client in self.clients:
            client.send(*args)

    async def close(self):
        await self.server.close()


class JankenClient:

    def __init__(self, server, connection):
        self.server = server
        self.connection = connection
        self.id = connection.address[1]
        self.logger = logging.getLogger('janken.client[%d]' % self.id)
        self.logger.info('connected')
        connection.on('action', self.on_action)
        connection.on('disconnect', self.on_disconnect)

    def send(self, *args):
        self.connection.send(*args)

    def on_action(self, action):
        self.server.battle.action(self, int(action))

    def on_disconnect(self):
        self.server.on_disconnect(self)
        self.logger.info('disconnected')


class JankenBattle:

    def __init__(self, server, clients):
        self.server = server
        self.clients = clients
        self.actions = []

    def action(self, client, action):
        assert(client in self.clients)
        self.actions.append((client, action, None))
        if len(self.actions) == len(self.clients):
            self.judge()

    def judge(self):
        actions = np.array(self.actions)
        uniq = np.unique(actions[:,1])
        if len(uniq) != 2:
            actions[:,2] = 0
        else:
            win = [2,1,3][uniq.sum()%3]
            actions[actions[:,1] == win, 2] = 1
            actions[actions[:,1] != win, 2] = -1
        self.server.judge(actions)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        loop = asyncio.get_event_loop()
        server = JankenServer()
        loop.run_until_complete(server.start(port=8888))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(server.close())
        loop.close()
