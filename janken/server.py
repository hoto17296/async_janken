import logging
import asyncio
import json
import numpy as np
from message import MessageServer


loop = asyncio.get_event_loop()


class Player:

    def __init__(self, connection):
        self.connection = connection
        self.id = connection.address[1]
        self.logger = logging.getLogger('janken.player[%d]' % self.id)
        self.logger.info('connected')

    async def ready(self, battle_id):
        future = loop.create_future()
        self.connection.send('ready', str(battle_id))

        @self.connection.once('action_%s' % battle_id)
        def on_action(action):
            if not future.done():
                future.set_result((self, int(action), None))

        try:
            return await asyncio.wait_for(future, timeout=1)
        except asyncio.TimeoutError:
            self.logger.info('timeout')
            return None

    def send(self, *args):
        self.connection.send(*args)


class JankenServer:

    def __init__(self):
        self.server = MessageServer()
        self.players = []
        self.battle_id = 0
        self.logger = logging.getLogger('janken.server')

        self.server.on('connect', self.on_connect)

    async def start(self, **kwargs):
        await self.server.start(**kwargs)
        while True:
            while len(self.players) < 2:
                self.logger.info('waiting...')
                await asyncio.sleep(1)
            await self.battle()
            self.battle_id += 1

    def on_connect(self, connection):
        player = Player(connection)
        self.players.append(player)
        connection.once('disconnect', lambda: self.players.remove(player))

    async def battle(self):
        self.logger.info('battle! id:%s' % self.battle_id)
        futures = [player.ready(self.battle_id) for player in self.players]
        actions = await asyncio.gather(*futures)
        actions = np.array(list(filter(lambda a: a is not None, actions)))
        if len(actions) < 2:
            self.logger.info('no contest')
            return
        for player, action, judge in self.judge(actions):
            action_str = ['✋', '✌', '✊'][action-1]
            judge_str = ['Lose...', 'Draw', 'Win!'][int(judge)+1]
            self.logger.info('%s %s %s' % (player.id, action_str, judge_str))
            player.send('judge', str(judge))

    def judge(self, actions):
        uniq = np.unique(actions[:,1])
        if len(uniq) != 2:
            actions[:,2] = 0
        else:
            win = [2,1,3][uniq.sum()%3]
            actions[actions[:,1] == win, 2] = 1
            actions[actions[:,1] != win, 2] = -1
        return actions

    async def close(self):
        await self.server.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        server = JankenServer()
        loop.run_until_complete(server.start(port=8888))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(server.close())
        loop.close()
