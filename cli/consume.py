from consumer import StompSyncConsumer
from config import AppConfig

# Third-Party Imports
from stompest.config import StompConfig
from signal import SIGINT, SIGTERM
import os

class CustomConsumer(StompSyncConsumer):
    """
    Consumes from the queue 'sigapabinho' by printing out the message.
    """
    queue = 'sigapabinho'
    stomp_config = StompConfig('tcp://{}:{}'.format(AppConfig.ACTIVEMQ['host'], AppConfig.ACTIVEMQ['port']),
                         version=AppConfig.ACTIVEMQ['stomp_version'])

    def __init__(self):
        """        
        Create a new Sync Consumer class instance.
        """
        super().__init__()
        self.stop = False

        # Define Signal handlers for SIGINT and SIGTERM
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
        with open('consumer_messages.txt', 'a+') as consumer_file:
            consumer_file.write('Got {}\n'.format(message.info()))
        
        return True
