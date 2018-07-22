# Third-party Imports
from multiprocessing import Process


class Supervisor(Process):
    """
    Supervisor object should launch as child processes/threads 
    and supervise the work of all its assigned consumers.
    """

    def __init__(self, consumers={}):
        """
        Supervisor class constructor.
            consumers (dict, optional): The mapping of consumer classes to number of desired consumers of the same.
        """
        Process.__init__(self, name="ConsumerSupervisor")
        self.assignedConsumers = consumers

    def assignConsumer(self, consumer):
        """
        Method which allows assigning consumers to a supervisor.
        
        Args:
            consumer (StompConsumer): An instance of a StompConsumer class or child classes.
        """
        self.assignedConsumers[consumer] = None

    def run(self):
        """        
        The supervisor process starts all the consumers 
        as its children and monitors their work.
        """
        # Start all assgined consumers
        for consumer in self.assignedConsumers.keys():

            # Start consumer
            print('Starting consumer...')
            self.assignedConsumers[consumer] = Process(target=consumer.run, name='CustomConsumer')
            self.assignedConsumers[consumer].start()
