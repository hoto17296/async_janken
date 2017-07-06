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
    logger.info('action: %s' % action)
    connection.send('action', str(action))

def strategy(info):
    return random.randint(1, 3)

@connection.on('issue')
def on_issue(issue):
    logger.info('issue: %s' % issue)

connection.connect('localhost', 8888)
