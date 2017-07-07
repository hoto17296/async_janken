import logging
import asyncio
import time
import numpy as np
from message import MessageConnection


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('janken.client')

connection = MessageConnection()

@connection.on('connect')
def on_connect():
    logger.info('connected')

@connection.on('disconnect')
def on_disconnect():
    logger.info('disconnected')

@connection.on('ready')
def on_ready(battle_id):
    action = strategy()
    action_str = ['✋', '✌', '✊'][action-1]
    logger.info('action: %s' % action_str)
    connection.send('action_%s' % battle_id, str(action))

def strategy():
    time.sleep(np.random.gamma(0.5,1.0))  # think
    return np.random.randint(1, 4)

@connection.on('judge')
def on_judge(judge):
    judge_str = ['Lose...', 'Draw', 'Win!'][int(judge)+1]
    logger.info('judge: %s' % judge_str)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(connection.connect('localhost', 8888))
    except KeyboardInterrupt:
        pass
    finally:
        connection.close()
        loop.close()
