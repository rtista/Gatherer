# Third-party Imports
from multiprocessing import Process
from signal import signal, SIGINT, SIGTERM


class Consumer(Process):
    """
    A Consumer is a process which consumes messages from a message queue system.
    
    Args:
        Process (multiprocessing.Process): An operation system process.
    """
    def __init__(self, conn_conf):
        """        
        Create a new Consumer class instance.
        """
        super().__init__()

        if conn_conf is None:
            raise ValueError('Connection configuration is None!')

        self.conn_conf = conn_conf

    def connect(self, conn_conf):
        """
        Connects to the MQ system using the conn_conf parameter.
        
        Args:
            conn_conf (Object): The MQ system connection client configuration.
        
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
        Returns whether the consumer can or not receive a message.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

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
