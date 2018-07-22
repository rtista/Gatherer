# Third-party Imports
from multiprocessing import Process
import time


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

    def startConsumer(self, consumer):
        """
        If possible, starts a new process for the given consumer.
        
        Args:
            consumer (StompConsumer): An instance of a StompConsumer class or child classes.
        """
        # Check if assigned consumers are not already running
        if self.assignedConsumers[consumer] == None or not self.assignedConsumers[consumer].is_alive():

            # Consumer was never started so start
            print('Starting consumer...')
            self.assignedConsumers[consumer] = Process(target=consumer.run)
            self.assignedConsumers[consumer].start()

        else:
            print('Nothing to do...')

    def stopConsumer(self, consumer):
        """
        If possible, stops a running consumer.
        
        Args:
            consumer (StompConsumer): An instance of a StompConsumer class or child classes.
        """
        # Check if assigned consumers are not already running
        if self.assignedConsumers[consumer].is_alive():

            # Stop consumer and release memory space associated
            print('Stopping consumer...')
            self.assignedConsumers[consumer].join()
            self.assignedConsumers[consumer].close()

        else:
            print('Nothing to do...')

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
        while True:

            print('Starting Consumers:')

            # Start all assigned consumers
            for consumer in self.assignedConsumers.keys():
                self.startConsumer(consumer)

            # Check if consumers are running every 10 sec
            time.sleep(10)