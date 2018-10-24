# Own Imports
from .consumer import QueueConsumer


class SyncConsumer(QueueConsumer):
    """
    Represents a Sync Consumer.
    """

    # A message queueing system adapter.
    adapter = None

    def __init__(self, adapter):
        """
        Create a new Sync Consumer class instance.
        
        Args:
            adapter (MQAdapter): A message queueing system adapter object.
        """
        super().__init__()
        self.adapter = adapter

    def run(self):
        """
        Contains the consumer main execution loop, will
        be executed on process start.
        """
        # Register mapped signal handlerss
        self.mapSignalHandlers()

        # Connect to the message system
        self.adapter.connect()

        # Subscribe to the queue
        self.adapter.subscribe(self.queue)

        # Sync Consumer Loop
        while self.can_consume():

            # Receive a message
            message = self.adapter.retrieve()

            # If there are messages to read
            if message is not None:

                # Consume the message
                if self.consume(message):

                    # Acknowledge the message
                    self.adapter.ack(message)
                else:
                    # Requeue the message
                    self.adapter.nack(message)

        # Disconnect from the MQ instance
        self.adapter.disconnect()
