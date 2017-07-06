"""
イベントループで日時を表示し続ける
"""

import asyncio
import datetime

def display_date(loop):
    print(datetime.datetime.now())
    loop.call_later(1, display_date, loop)

loop = asyncio.get_event_loop()  # イベントループを取得する
loop.call_soon(display_date, loop)  # スケジューリング
try:
    loop.run_forever()  # イベントループを実行する
except KeyboardInterrupt:
    loop.stop()  # イベントループを停止する
    loop.close()  # イベントループを閉じる
