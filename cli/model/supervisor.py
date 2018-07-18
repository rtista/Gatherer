# Third-party Imports
from multiprocessing import Process


class Supervisor(Process):
    """
    Supervisor object should launch as child processes/threads 
    and supervise the work of all its assigned consumers.
    """

    def __init__(self, consumers=[]):
        """
        Supervisor class constructor.
        """
        Process.__init__(self, name="ConsumerSupervisor")
        self.assignedConsumers = consumers

    def assignConsumer(self, consumer):
        """
        Method which allows assigning consumers to a supervisor.
        
        Args:
            consumer (StompConsumer): An instance of the StompConsumer class, or child classes.
        """
        self.assignedConsumers.append(consumer)

    def run(self):
        """        
        The supervisor process starts all the consumers 
        as its children and monitors their work.
        """
        # Start all assgined consumers
        for consumer in self.assignedConsumers:
            print('Starting consumer...')
            Process(target=consumer.run, name='CustomConsumer').start()
