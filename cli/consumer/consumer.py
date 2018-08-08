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

    def connect(self):
        """
        Connects to the MQ system using the conn_conf parameter.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def subscribe(self, client):
        """
        Subscribes to the designated queue.
        
        Args:
            client (Object): The MQ system connection client.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def can_consume(self):
        """
        Returns whether the consumer should consume messages or stop execution.

        Returns:
            Boolean : Whether the consumer should consume messages or stop (default is True)
        """
        return True

    def receive(self, client):
        """
        Gets a message from the message system and returns it.
        
        Args:
            client (Object): The MQ system connection client.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

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

    def ack(self, client, message):
        """
        Acknowledges the given message.
        
        Args:
            client (Object): The MQ system connection client.
            message (Object): A MQ system message.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def nack(self, client, message):
        """
        Not acknowledges the given message.
        
        Args:
            client (Object): The MQ system connection client.
            message (Object): A MQ system message.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def disconnect(self, client):
        """
        Disconnects from the Message Queueing System.
        
        Args:
            client (Object): The MQ system connection client.
        
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
