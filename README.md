# [asyncio](https://docs.python.org/3/library/asyncio.html) practice
Requires Python 3.5 or higher.

## Janken
Install [pyee](https://pypi.python.org/pypi/pyee).

``` console
$ pip install pyee
```

Start Janken server.

``` console
$ python janken/server.py
```

Run multiple Janken clients.

``` console
$ seq 3 | xargs -I{} -P 3 python janken/client.py
```
