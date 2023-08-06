# dock

Wrapper around Redis for message queues.

## Installation

```bash
pip install dock  # pypi
pip install git+https://github.com/vzhong/dock.git  # github
```

## Usage

First, start your Redis server.

```python
# server.py
from dock import Dock
dock = Dock('test')

while True:
    msg, respond = dock.recv()
    print(msg, respond)
    print('got message {}'.format(msg))
    respond({
      'ack': msg,
      'msg': 'hello'
    })
```

```python
# client.py
from dock import Dock
dock = Dock('test')

for i in range(5):
    answer = dock.send('message{}'.format(i))
    print(answer)
```

You can see how the server and client interact by running the two files:

```bash
python server.py  # in one terminal
python client.py  # in another terminal
```
