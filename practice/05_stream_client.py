import asyncio

loop = asyncio.get_event_loop()

future = asyncio.open_connection('localhost', 8888)
reader, writer = loop.run_until_complete(future)

def publish(data):
    if type(data) is str:
        data = (data+'\n').encode('utf-8')
    writer.write(data)

async def subscribe():
    while True:
        data = await reader.readline()
        if data:
            print(data)
        else:
            print('connection closed')
            break

publish('send from client!')

try:
    loop.run_until_complete(subscribe())
except KeyboardInterrupt:
    pass
finally:
    writer.close()
    loop.close()
