# Imports
from .unix import UnixProcess


class QueueConsumer(UnixProcess):
    """
    A Consumer is a Unix Process which consumes messages 
    from a queue that belongs in message queue system.
    """

    # The queue from which to consume messages
    queue = None

    def __init__(self):
        """        
        Create a new Consumer class instance.
        """
        super().__init__(name='Consumer')

    def can_consume(self):
        """
        Returns whether the consumer should consume messages or stop execution.

        Returns:
            Boolean : Whether the consumer should consume messages or stop (default is True)
        """
        return True

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.
        
        Args:
            message (Object): A MQ system message.
        
        Returns:
            Boolean: Whether the message should or not be acknowledged.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def run(self):
        """
        Contains the consumer main execution loop, will be executed on process start.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')
