# Import Configuration
from config import AppConfig
from .listener import UnixListener

# Third-party Imports
from multiprocessing import Process
from multiprocessing.connection import Listener
from threading import Thread
from signal import signal, SIGTERM, SIGINT, SIGKILL
from os import fork, kill, getpid, unlink
import time
import inspect


class ConsumerSupervisor(Process):
    """
    Supervisor object should launch as child processes 
    and supervise the work of all its assigned processes.
    """

    # Assigned Processes Map
    # Holds all information relative to assigned processes, 
    # running child instances and monitored instances.
    # i.e. {
    #   class.__name__ : {
    #       'class': Consumer,
    #       'monitored': 2,
    #       'running': []
    #   },
    #   (...)
    # }
    assigned = {}

    def __init__(self, assigned_processes={}):
        """
        Supervisor class constructor.
        """
        Process.__init__(self, name='Supervisor')
        self.stop = False

        # Assign given processes
        for process in assigned_processes.keys():
            self.assignProcess(process, assigned_processes[process])

    def assignProcess(self, process, count):
        """
        Method which allows assigning a process to the supervisor.
        
        Args:
            process (multiprocessing.Process): A non-abstract child class of the Process class.
            count (int): The number of instances to keep running concurrently.
        """
        if inspect.isclass(process) and count > 0 and process.__name__ not in self.assigned.keys():

            self.assigned[process.__name__] = {
                'class': process,
                'monitored': count,
                'running': []
            }

    def spawnInstance(self, process):
        """
        Spawns an instance of an assigned process.
        
        Args:
            process (str): The name of the process class to start.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist 
        if process not in self.assigned.keys():
            return False

        # Start a new process for the consumer
        print('Starting instance of {}...'.format(process))

        instance = self.assigned[process]['class']()

        instance.start()

        self.assigned[process]['running'].append(instance)

        return True

    def stopInstance(self, process):
        """
        If possible, stops a running instance of an assigned process.
        
        Args:
            process (str): The name of the process class to start.

        Returns:
            boolean : Success of the operation.
        """
        # Return false if the consumer does not exist 
        if process not in self.assigned.keys():
            return False

        # Check if there are any processes running
        if len(self.assigned[process]['running']) == 0:
            return False

        # Remove the process from the list of running
        instance = self.assigned[process]['running'].pop(0)

        # Stop process and release memory space associated
        print('Stopping instance of {}...'.format(process))

        # Stop the consumer cycle
        kill(instance.pid, SIGTERM)

        # Wait for process to die for 10 secondes
        instance.join(timeout=7)

        return True

    def monitInstances(self):
        """    
        Monitors all the assigned process and its respective instances.
        """
        for process in self.assigned.keys():

            # Remove dead processes from running
            running = []

            for instance in self.assigned[process]['running']:

                # If the process is running
                if instance.is_alive():
                    running.append(instance)

            # Override old processlist by new
            self.assigned[process]['running'] = running

            dif = self.assigned[process]['monitored'] - len(self.assigned[process]['running'])

            if dif > 0:
                map(self.spawnInstance(process), range(abs(dif)))

            elif dif < 0:
                map(self.stopInstance(process), range(abs(dif)))


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
        # Double-fork allows background running
        if fork() != 0:
            return

        # Declare signal handler
        signal(SIGTERM, self.sighandler)
        signal(SIGINT, self.sighandler)

        # Create PID file
        with open(AppConfig.PID_LOCATION, 'w') as pidfile:
            pidfile.write(str(getpid()))

        # TODO Have UNIX_AF listener - Requires Thread...
        unixsock = Listener(AppConfig.UNIX_SOCKET, 'AF_UNIX')

        # Spawn listener thread
        UnixListener(unixsock, self.assigned).start()

        # Main Loop
        while self.canSupervise():

            # Monitor assigned consumers every 10 sec
            self.monitInstances()

            # Sleep 10 sec
            time.sleep(1)

        print('Supervisor: Stoping all children....')

        # Stop all running consumers
        for process in self.assigned.keys():
            while len(self.assigned[process]['running']) > 0:
                self.stopInstance(process)
                time.sleep(0.2)

        # Close unixsocket
        unixsock.close()

        # Close everything / remove PID file
        unlink(AppConfig.PID_LOCATION)