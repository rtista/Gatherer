# Import Configuration
from config import AppConfig

# Third-party Imports
from multiprocessing import Process
from signal import signal, SIGTERM, SIGINT, SIGKILL
from os import kill, getpid, unlink
import time


class ConsumerSupervisor(Process):
    """
    Supervisor object should launch as child processes 
    and supervise the work of all its assigned processes.
    """

    def __init__(self):
        """
        Supervisor class constructor.
        """
        Process.__init__(self, name='Supervisor')
        self.stop = False
        self.consumermap = {}

    def assignConsumer(self, consumer):
        """
        Method which allows assigning a consumer to the supervisor.
        
        Args:
            consumer (QueueConsumer): A non-abstract child class of the QueueConsumer class.
        """
        if consumer not in self.consumermap.keys():
            self.consumermap[consumer] = []

    def startConsumer(self, consumer):
        """
        Starts a process of an assigned consumer.
        
        Args:
            consumer (class): The consumer class to start.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist 
        if consumer not in self.consumermap.keys():
            return False

        # Start a new process for the consumer
        print('Starting consumer {}...'.format(consumer))

        process = consumer()

        process.start()

        self.consumermap[consumer].append(process)

        return True

    def stopConsumer(self, consumer):
        """
        If possible, stops a running consumer.
        
        Args:
            consumer (class): The class of the assigned consumer to stop.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist
        if consumer not in self.consumermap.keys():
            return False

        # Check if there are any processes running
        if len(self.consumermap[consumer]) == 0:
            return False

        # Remove the process from the list of running
        process = self.consumermap[consumer].pop(0)

        # Stop process and release memory space associated
        print('Stopping consumer {}...'.format(consumer))

        # Stop the consumer cycle
        kill(process.pid, SIGTERM)

        # Wait for process to die for 10 secondes
        process.join(timeout=10)

        return True

    def monitorConsumers(self):
        """    
        Monitors all the assigned consumers and respective processes.
        """
        for consumer in self.consumermap.keys():

            if len(self.consumermap[consumer]) < 1:
                self.startConsumer(consumer)

            # Remove dead processes from proclist
            proclist = []

            for proc in self.consumermap[consumer]:
                # If the process is not running
                if proc.is_alive():
                    proclist.append(proc)

            # Override old processlist by new
            self.consumermap[consumer] = proclist

    def canSupervise(self):
        """
        Allows gracefully stopping the supervisor if needed.
        
        Returns:
            boolean: Whether the supervisor should keep running.
        """
        return self.stop == False

    def sighandler(self, signum, frame):
        """
        Supervisor signal handler function.
        
        Args:
            signum (int): The signal received.
            frame (frame): The process which killed this one.
        """
        self.stop = True

    def run(self):
        """
        The supervisor process starts all its assigned processes 
        as its children and monitors their work.
        """
        # Declare signal handler
        signal(SIGTERM, self.sighandler)
        signal(SIGINT, self.sighandler)

        # Create PID file
        with open(AppConfig.PID_LOCATION, 'w') as pidfile:
            pidfile.write(str(getpid()))

        # TODO Have UNIX_AF listener

        # Start assigned consumers
        print('Starting Assigned Processes:')
        map(self.startConsumer, self.consumermap.keys())

        # Main Loop
        while self.canSupervise():

            # Monitor assigned consumers
            self.monitorConsumers()

            # Check if processes are running every 10 sec
            time.sleep(10)

        print('Supervisor: Stoping all children....')

        # Stop all running consumers
        for consumer in self.consumermap.keys():
            self.stopConsumer(consumer)

        # Close everything / remove PID file
        unlink(AppConfig.PID_LOCATION)