# Third-party Imports
from stompest.protocol import StompSpec

# Third-party imports
from multiprocessing import Process
from stompest.sync import Stomp


class StompConsumer(object):
    """
    A StompConsumer is a process which consumes messages from a stomp connection.
    
    Args:
        Process (multiprocessing.Process): An operation system process.
    """

    def __init__(self, queue=None, stomp_config=None, consumer_id=None, headers=None):
        """        
        Create a new Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The Stomp connection configuration object.
            consumer_id (string): The consumer id, an alfanumeric string.
            headers (Dict): The Stomp connection headers to be used.
        """
        # Check for invalid values
        if None in [queue, stomp_config, consumer_id]:
            raise ValueError('Invalid consumer parameters.')

        # Assign values
        self.queue = queue
        self.consumer_id = consumer_id
        self.headers = headers
        self.conn = self.connect(stomp_config)

    def connect(self, stomp_config):
        """
        Connects to the Message Queueing System.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def subscribe(self):
        """
        Subscribes to the designated queue.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def consume(self):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def disconnect(self):
        """
        Disconnects from the Message Queueing System.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')

    def run(self):
        """
        Starts the consumer.
        
        Raises:
            NotImplementedError: This is an abstract function.
        """
        raise NotImplementedError('This is an abstract function.')


class SyncStompConsumer(StompConsumer):
    """
    Represents a Sync Stomp Consumer.
    """
    def __init__(self, queue, stomp_config, consumer_id, headers):
        """        
        Create a new Sync Consumer class instance.
        
        Args:
            queue (string): The queue, from which to consume, name.
            stomp_config (StompConfig): The Stomp sync connection configuration object.
            headers (Dict): The Stomp connection headers to be used.
        """
        super().__init__(queue, stomp_config, consumer_id, headers)

    def connect(self, stomp_config):
        """
        Connects to the Message Queueing System.

        Args:
            stomp_config (stompest.Config.StompConfig): The Stomp connection configuration.
        
        Returns:
            stompest.sync.Stomp: The Stomp connection client.
        """
        client = Stomp(stomp_config)
        client.connect()
        return client

    def subscribe(self):
        """
        Subscribes to the designated queue.
        
        Returns:
            str: The queue subscribed to.
        """
        self.conn.subscribe(self.queue, self.headers)
        return self.queue

    def consume(self, message):
        """
        Receives a message or group of messages, processes 
        them and acknowledges them.
        
        Raises:
            NotImplementedError: This is an abstract function.

        Returns:
            boolean: Whether the message should or not be acknowledged.
        """
        raise NotImplementedError('This is an abstract function.')

    def disconnect(self):
        """
        Disconnects from the Message Queueing System.
        """
        self.conn.disconnect()

    def run(self):
        """
        Starts the consumer.
        """
        print('Subscribing to {} queue...'.format(self.subscribe()))

        # Consumer Loop
        while True:
            # Receive a message
            message = self.conn.receiveFrame()

            # Consume the message
            if self.consume(message):

                # Acknowledge the message
                self.conn.ack(message)
            else:
                # Requeue the message
                self.conn.nack(message)

        # Disconnect from the MQ instance
        self.disconnect()