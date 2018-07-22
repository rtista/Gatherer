# Own Imports
from .consumer import Consumer

class SyncConsumer(Consumer):
    """
    Represents a Sync Consumer.
    """
    def __init__(self, conn_conf):
        """        
        Create a new Sync Consumer class instance.
        """
        super().__init__(conn_conf)

    def run(self):
        """
        Contains the consumer main execution loop, will
        be executed on process start.
        """
        # Connect to the message system
        client = self.connect(self.conn_conf)

        # Subscribe to the queue
        self.subscribe(client)

        # Sync Consumer Loop
        while self.can_consume():

            # Receive a message
            message = self.receive(client)

            # Consume the message
            if self.consume(message):

                # Acknowledge the message
                self.ack(client, message)
            else:
                # Requeue the message
                self.nack(client, message)

        # Disconnect from the MQ instance
        self.disconnect(client)