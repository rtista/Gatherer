# Own Imports
from .abstract import MQAdapter

# Third Party Imports
from stompest.sync import Stomp
from stompest.config import StompConfig
from stompest.protocol.spec import StompSpec

class StompMQAdapter:
    """
    Represents a Message Queueing adapter, an object
    capable of interacting with a MQ system via Stomp protocol.
    """

    # The Stomp connection headers.
    headers = { StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL }

    def __init__(self, host, port, version, headers={}):
        """
        Creates an instance of the StompMQAdapter class.

        Args:
            host (str): Hostname or IP address for locating the MQ system.
            port (int): The port to connect to.
            stomp_version (str): The Stomp protocol version ot be used.
            headers (dict, optional): Defaults to {}. The headers to be used in the connection.
        """
        self.client = Stomp(StompConfig('tcp://{}:{}'.format(host, port),
                            version=version))

        # Assign mandatory ID_HEADER if version above 1.1
        if float(version) > 1.1:
            self.headers[StompSpec.ID_HEADER] = id(self.client)

        # Add all given headers to object headers
        for key in headers.keys():
            self.headers[key] = headers[key]

    def connect(self):
        """
        Connects to the MQ system via Stomp protocol.

        Raises:
            StompConnectTimeout: Could not connect to STOMP socket.
        """
        self.client.connect()

    def subscribe(self, queue):
        """
        Subscribes to a queue in the MQ system.

        Args:
            queue (str): The queue to subscribe to.
        """
        self.client.subscribe(queue, self.headers)

    def queue(self, queue, message):
        """
        Sends a message to the specified queue.

        Args:
            queue (str): The queue to where the message should be queued.
            message: The message to be queued.

        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        self.client.send(queue, message.encode())

    def retrieve(self):
        """
        Retrieves a message from the subscription (queue).

        Returns:
            object: The message to be consumed or None if the queue is empty.
        """
        if self.client.canRead(timeout=2):
            return self.client.receiveFrame()

        return None

    def ack(self, message):
        """
        Acknowledges the consumption of the given message.

        Args:
            message ([type]): The message to be acknowledged.
        """
        self.client.ack(message)

    def nack(self, message):
        """
        Not-acknowledges the consumption of the given message.

        Args:
            message ([type]): The message to be not-acknowledged.
        """
        self.client.nack(message)

    def disconnect(self):
        """
        Disconnects from the MQ system.
        """
        self.client.disconnect()