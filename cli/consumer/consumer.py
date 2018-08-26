# Import multiprocessing.Process class
from multiprocessing import Process


class QueueConsumer(Process):
    """
    A Consumer is a process which consumes messages 
    from a queue that belongs in message queue system.
    """

    # The queue from which to consume messages
    queue = None

    def __init__(self):
        """        
        Create a new Consumer class instance.
        """
        Process.__init__(self, name='Consumer')
        self.sigmap = {}

    def addSighandler(self, sig, sighandler):
        """
        Allows adding handler functions for unix signals.

        Args:
            sig (int): The signal to be handled.
            sighandler (function): The handler function.
        """
        self.sigmap[sig] = sighandler

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
