import logging
import asyncio
from message import MessageClient


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    MessageClient().connect('localhost', 8888)
