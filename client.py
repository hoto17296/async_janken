import logging
import asyncio
from message import MessageClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('janken.client')

client = MessageClient()

@client.on('connect')
def on_connect():
    logger.info('connected')

@client.on('disconnect')
def on_disconnect():
    logger.info('disconnected')

client.connect('localhost', 8888)
