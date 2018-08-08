# Own Imports
from .sync import SyncConsumer

# Third-party Imports
from stompest.sync import Stomp
from stompest.protocol.spec import StompSpec

class StompSyncConsumer(SyncConsumer):
    """
    Represents a Sync Stomp Consumer.

    The class assigns automatically the ACK_CLIENT_INDIVIDUAL 
    ACK_HEADER to allow concurrent consuming fro the same queue.
    """
    stomp_config = None
    stomp_headers = { StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL }

    def __init__(self):
        """        
        Create a new Sync Stomp Consumer class instance.
        """
        super().__init__()

        # Check if stomp configuration is valid
        if self.stomp_config is None:
            raise ValueError('Stomp Configuration object is empty.')

        # Assign mandatory ID_HEADER if version above 1.1
        if float(self.stomp_config.version) > 1.1:
            self.stomp_headers[StompSpec.ID_HEADER] = id(self)

    def connect(self):
        """
        Connects to the MQ system using the conn_conf parameter.
        
        Raises:
            StompConnectTimeout: Could not connect to STOMP socket.
        """
        client = Stomp(self.stomp_config)
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
        client.subscribe(self.queue, self.stomp_headers)

    def receive(self, client):
        """
        Gets a message from the message system and returns it.
        
        Args:
            client (Object): The MQ system connection client.

        Returns:
            object: A message to be consumed or 'None' if there are no messages to read.
        """
        if client.canRead(2):
            return client.receiveFrame()

        return None

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