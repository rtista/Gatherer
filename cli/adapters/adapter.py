class MQAdapter:
    """
    Represents a Message Queueing adapter, an object 
    capable of interacting with a MQ system.
    """
    
    # The client capable of communicating with the MQ system.
    client = None

    def connect(self):
        """
        Connects to the MQ system.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

    def queue(self, message, queue):
        """
        Sends a message to the specified queue.
        
        Args:
            message: The message to be queued.
            queue (str): The queue to where the message should be queued.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

    def retrieve(self, queue):
        """
        Retrieves a message from the specified queue.
        
        Args:
            queue (str): The queue from where to retrieve the message.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

    def ack(self, message):
        """
        Acknowledges the consumption of the given message.
        
        Args:
            message ([type]): The message to be acknowledged.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

    def nack(self, message):
        """
        Not-acknowledges the consumption of the given message.
        
        Args:
            message ([type]): The message to be not-acknowledged.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

    def disconnect(self):
        """
        Disconnects from the MQ system.
        
        Raises:
            NotImplementedError: Implement this method on a child class.
        """
        raise NotImplementedError('Implement this method on a child class.')

