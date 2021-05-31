# pySockets

![](/images/ss1.png)

## Usage:

1. SERVER-

```python
python3 server.py -p PORT -i IP_ADDRESS
```

2. CLIENT-

```python
python3 client.py -p PORT -i IP_ADDRESS_OF_SERVER -u USER
```

## Features:

1. Multi-threading allows multiple users to send and receive messages simultaneously.

2. Messages when sent from server to client or vice versa are encoded with AES CBC mode, with each message having a unique IV (initialization vector).
