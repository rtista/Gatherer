from consumer import StompSyncConsumer

# Third-Party Imports
from stompest.protocol.spec import StompSpec
from signal import SIGINT, SIGTERM
import os

class CustomConsumer(StompSyncConsumer):
    """
    My consumer is the best consumer.
    """
    def __init__(self, queue, stomp_config):
        """        
        Create a new Sync Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The Stomp sync connection configuration object.
            consumer_id (string): A unique ID for the consumer.
        """
        super().__init__(queue, stomp_config, 
                        {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL,
                        StompSpec.ID_HEADER: id(self) }
                        )
        self.stop = False
        self.addSighandler(SIGINT, self.sighandler)
        self.addSighandler(SIGTERM, self.sighandler)

    def sighandler(self, signum, frame):
        """
        Sets stop to True so the consumer stops
        consuming and terminates itself.
        
        Args:
            signum (int): The signal received.
            frame (frame): The process which killed this one.
        """
        self.stop = True

    def can_consume(self):
        """
        Returns whether the consumer should keep 
        consuming messages or stop.
        """
        return self.stop == False

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.

        Returns:
            boolean 
        """
        print('Got {}'.format(message.info()))
        
        return True
