# Own Imports
from .sync import SyncConsumer

# Third-party Imports
from stompest.sync import Stomp

class StompSyncConsumer(SyncConsumer):
    """
    Represents a Sync Stomp Consumer.
    """
    def __init__(self, queue, stomp_config, headers):
        """        
        Create a new Sync Stomp Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The stomp connection configuration object.
        """
        super().__init__(stomp_config)

        if queue is None:
            raise ValueError('Queue object is empty.')

        self.queue = queue
        self.headers = headers

    def connect(self, conn_conf):
        """
        Connects to the MQ system using the conn_conf parameter.
        
        Args:
            conn_conf (StompConfig): The MQ system stomp connection client configuration.
        
        Raises:
            StompConnectTimeout: Could not connect to STOMP socket.
        """
        client = Stomp(conn_conf)
        client.connect()
        return client

    def subscribe(self, client):
        """
        Subscribes to the designated queue.
        
        Args:
            client (Stomp): The MQ system connection client.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        client.subscribe(self.queue, self.headers)

    def receive(self, client):
        """
        Gets a message from the message system and returns it.
        
        Args:
            client (Object): The MQ system connection client.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        return client.receiveFrame()

    def ack(self, client, message):
        """
        Acknowledges the given message.
        
        Args:
            message (Object): A MQ system message.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        client.ack(message)

    def nack(self, client, message):
        """
        Not acknowledges the given message.
        
        Args:
            message (Object): A MQ system message.

        Raises:
            NotImplementedError: This is an abstract function.
        """
        client.nack(message)

    def disconnect(self, client):
        """
        Disconnects from the Message Queueing System.
        
        Args:
            client (Object): The MQ system connection client.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        client.disconnect()