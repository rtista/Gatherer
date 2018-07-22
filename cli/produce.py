from stompest.config import StompConfig
from stompest.sync import Stomp
from random import choice

stompconf = StompConfig('tcp://127.0.0.1:61613', version='1.2')
QUEUE = '/queue/sigapabinho'

if __name__ == '__main__':
    client = Stomp(stompconf)
    client.connect()

    while True:
        client.send(QUEUE, 'test message {}'.format(choice(range(0, 10))).encode())
    
    client.disconnect()