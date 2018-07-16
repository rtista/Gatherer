from abstract import SyncStompConsumer

import os

class CustomConsumer(SyncStompConsumer):
    """
    My consumer is the best consumer.
    """
    def __init__(self, queue, stomp_config, headers):
        """        
        Create a new Sync Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The Stomp sync connection configuration object.
            headers (Dict): The Stomp connection headers to be used.
        """
        super().__init__(queue, stomp_config, headers)

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.

        Returns:
            boolean
        """
        print('Got {}'.format(message.info()))
        
        return True

from stompest.config import StompConfig
from stompest.protocol import StompSpec

stompconf = StompConfig('tcp://127.0.0.1:61613',
                        version='1.2')

CustomConsumer('/queue/sigapabinho', stompconf, {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL, 
                                                 StompSpec.ID_HEADER: os.getpid()}).run()