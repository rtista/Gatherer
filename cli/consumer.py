from model import SyncStompConsumer

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
