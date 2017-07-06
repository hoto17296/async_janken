import logging
import asyncio
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

connection.connect('localhost', 8888)
