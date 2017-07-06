import asyncio
import sys
import random

def random_hit(loop, future, n_upper, count=1):
    value = random.randint(1, n_upper)
    if value == 1:
        return future.set_result(count)
    loop.call_soon(random_hit, loop, future, n_upper, count+1)

def callback(future):
    print('done')

loop = asyncio.get_event_loop()
future = loop.create_future()
future.add_done_callback(callback)
loop.call_soon(random_hit, loop, future, 4)
result = loop.run_until_complete(future)
print(result)
loop.close()
