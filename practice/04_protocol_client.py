# http://docs.python.jp/3/library/asyncio-protocol.html#tcp-echo-client-protocol

import asyncio

class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'Hello World!'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop), '127.0.0.1', 8888)
loop.run_until_complete(coro)  # 接続できない場合はここで例外が上がる
loop.run_forever()  # 実際のイベントループ実行はこっち
loop.close()
