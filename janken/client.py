import logging
import asyncio
import random
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
def on_ready(info):
    action = strategy(info)
    action_str = ['✋', '✌', '✊'][action-1]
    logger.info('action: %s' % action_str)
    connection.send('action', str(action))

def strategy(info):
    return random.randint(1, 3)

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
