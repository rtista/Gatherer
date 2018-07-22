from consumer import StompSyncConsumer

# Third-Party Imports
from stompest.protocol.spec import StompSpec
import os

class CustomConsumer(StompSyncConsumer):
    """
    My consumer is the best consumer.
    """
    def __init__(self, queue, stomp_config, consumer_id):
        """        
        Create a new Sync Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The Stomp sync connection configuration object.
            consumer_id (string): A unique ID for the consumer.
        """
        super().__init__(queue, stomp_config, 
                        {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL,
                        StompSpec.ID_HEADER: consumer_id}
                        )

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.

        Returns:
            boolean 
        """
        print('Got {}'.format(message.info()))
        
        return True
