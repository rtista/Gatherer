# Third-party Imports
from multiprocessing import Process
from signal import signal, SIGTERM, SIGINT, SIGKILL
from os import kill
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
        Process.__init__(self, name="Supervisor")
        self.stop = False
        self.consumermap = {}
        self.processmap = {}

    def assignConsumer(self, name, consumer):
        """
        Method which allows assigning a consumer to the supervisor.
        
        Args:
            name (String): An unique identifier for the consumer.
            consumer (QueueConsumer): An instance of a Consumer class or child classes.
            count (int): Number of consumer processes to keep running.
        """
        if name not in self.consumermap.keys():
            self.consumermap[name] = consumer
            self.processmap[name] = []

    def startConsumer(self, name):
        """
        Starts a process of an assigned consumer.
        
        Args:
            name (string): The name of the assigned consumer to start.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist 
        if name not in self.consumermap.keys():
            return False

        # Start a new process for the consumer
        print('Starting consumer {}...'.format(name))
        process = Process(target=self.consumermap[name].run)
        self.processmap[name].append(process)
        process.start()

        return True

    def stopConsumer(self, name):
        """
        If possible, stops a running consumer.
        
        Args:
            name (string): The name of the assigned consumer to stop.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist
        if name not in self.consumermap.keys():
            return False

        # Check if there are any processes running
        if len(self.processmap[name]) == 0:
            return False

        # Remove the process from the list of running
        process = self.processmap[name].pop(0)

        # Stop process and release memory space associated
        print('Stopping consumer {}...'.format(name))

        # Stop the consumer cycle
        kill(process.pid, SIGTERM)

        # Wait for process to die for 10 secondes
        process.join(timeout=10)

        # If process did not terminate, kill it
        if process.exitcode != -15:
            print('Exitcode: {} PID: {}'.format(process.exitcode, process.pid))
            kill(process.pid, SIGKILL)

        return True

    def canSupervise(self):
        """
        Allows gracefully stopping the supervisor if needed.
        
        Returns:
            boolean: Whether the supervisor should keep running.
        """
        return self.stop == False

    def stopSupervisor(self):
        """
        Stops all consumers and supervisor process.
        """
        print('Stopping supervisor...')

        # Stop the supervisor
        self.stop = True

    def sighandler(self, signum, frame):
        """
        Supervisor signal handler function.
        
        Args:
            signum (int): The signal received.
            frame (frame): The process which killed this one.
        """
        print('Received signal {} and frame: {}'.format(signum, frame))
        self.stopSupervisor()

    def run(self):
        """
        The supervisor process starts all its assigned processes 
        as its children and monitors their work.
        """
        # Declare signal handler
        signal(SIGTERM, self.sighandler)
        signal(SIGINT, self.sighandler)

        # TODO Create PID file

        # TODO Have UNIX_AF listener

        # Main Loop
        while self.canSupervise():

            print('Starting Assigned Processes:')

            # Start all assigned processes
            for name in self.consumermap.keys():

                # Start at least 1 process for each assigned consumer
                if len(self.processmap[name]) < 1:
                    self.startConsumer(name)


            # Check if processes are running every 10 sec
            time.sleep(10)

        print('Supervisor is stopping....')

        # Stop all running consumers
        for name in self.processmap.keys():
            for proc in self.processmap[name]:
                self.stopConsumer(name)

        # Close everything / remove PID file