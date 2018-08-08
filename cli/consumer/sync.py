# Own Imports
from .consumer import QueueConsumer

# Third-party Imports
from signal import signal


class SyncConsumer(QueueConsumer):
    """
    Represents a Sync Consumer.
    """
    def __init__(self):
        """        
        Create a new Sync Consumer class instance.
        """
        super().__init__()

    def run(self):
        """
        Contains the consumer main execution loop, will
        be executed on process start.
        """
        # Register configured signal handlers
        for key in self.sigmap:
            signal(key, self.sigmap[key])

        # Connect to the message system
        client = self.connect()

        # Subscribe to the queue
        self.subscribe(client)

        # Sync Consumer Loop
        while self.can_consume():

            # Receive a message
            message = self.receive(client)

            # If there are messages to read
            if message is not None:

                # Consume the message
                if self.consume(message):

                    # Acknowledge the message
                    self.ack(client, message)
                else:
                    # Requeue the message
                    self.nack(client, message)

        # Disconnect from the MQ instance
        self.disconnect(client)
