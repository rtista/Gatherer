# Own Imports
from adapters import StompMQAdapter
from config import AppConfig

# Third party imports
from random import choice

# The queue from which it will consume
queue = 'sigapabinho'

if __name__ == '__main__':

    # Message Queue System Adapter
    adapter = StompMQAdapter(
        AppConfig.ACTIVEMQ['host'],
        AppConfig.ACTIVEMQ['port'],
        AppConfig.ACTIVEMQ['stomp_version']
    )

    try:
        adapter.connect()
        
    except Exception:
        print('Could not connect to ActiveMQ instance.')
        exit(1)

    while True:
        adapter.queue(queue, 'test message {}'.format(choice(range(0, 10))))
    
    adapter.disconnect()