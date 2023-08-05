# A simple queue lib base on sqlite3

----------

Feature:
- Local disk queue base on sqlite3
- Simple and easy to use


Usage:

```python

from sqlqueue import Queue
queue = Queue('myqueue')

print queue.get_nowait()
>>> None

queue.put('sqlqueue')
queue.put(1)
queue.put({'foo':1, 'bar':2})

print queue.get_nowait()
>>> 'sqlqueue'
print queue.get_nowait()
>>> 1
print queue.get_nowait()
>>> {'bar': 2, 'foo': 1}

```


This is a copy from [http://flask.pocoo.org/snippets/88/](http://flask.pocoo.org/snippets/88/) with little alternation



