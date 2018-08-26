# Own Imports
from config import AppConfig
from consumer import SyncConsumer
from adapters import StompMQAdapter

# Third-Party Imports
from signal import SIGINT, SIGTERM


class CustomConsumer(SyncConsumer):
    """
    Consumes from the queue 'sigapabinho' by printing out the message.
    """

    # The queue from which it will consume
    queue = 'sigapabinho'

    # Message Queue System Adapter
    adapter = StompMQAdapter(
        AppConfig.ACTIVEMQ['host'],
        AppConfig.ACTIVEMQ['port'],
        AppConfig.ACTIVEMQ['stomp_version']
    )

    def __init__(self):
        """        
        Create a new Sync Consumer class instance.
        """
        super().__init__(self.adapter)
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
        
        Returns:
            boolean: Whether the consumer should or not stop execution.
        """

        return self.stop == False

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.
        
        Args:
            message (StompFrame): The message to be consumed.
        
        Returns:
            boolean: Whether the message should or not be acknowledged.
        """
        with open('consumer_messages.txt', 'a+') as consumer_file:
            consumer_file.write('Got {}\n'.format(message.info()))
        
        return True
