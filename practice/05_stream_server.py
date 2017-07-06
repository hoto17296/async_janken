import asyncio

async def handler(reader, writer):
    address = writer.get_extra_info('peername')
    print(address)

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

    publish('send from server!')
    return await subscribe()

loop = asyncio.get_event_loop()

try:
    future = asyncio.start_server(handler, port=8888)
    server = loop.run_until_complete(future)
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
