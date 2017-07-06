import asyncio

# asyncio.sleep の簡易版
async def sleep(delay):
    if delay == 0:
        return
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    loop.call_later(delay, future.set_result, None)
    return (await future)

# n 回までカウントするカウンタ
async def counter(id, n):
    for i in range(n):
        print("id: {}, count: {}".format(id, i))
        await sleep(0.5)
    print("FINISH! id: {}".format(id))

loop = asyncio.get_event_loop()

# コルーチンのリスト
futures = [counter(i, 3) for i in range(3)]

# すべてのコルーチンが完了するまで待つコルーチン
coroutine = asyncio.wait(futures)

# コルーチンが完了するまでイベントループを回す
loop.run_until_complete(coroutine)

loop.close()
