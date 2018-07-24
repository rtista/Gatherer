# Third-party Imports
from multiprocessing import Process
import time
from copy import copy

class Supervisor(Process):
    """
    Supervisor object should launch as child processes 
    and supervise the work of all its assigned processes.
    """

    def __init__(self):
        """
        Supervisor class constructor.
        """
        Process.__init__(self, name="Supervisor")
        self.assignedProcesses = {}
        self.runningProcesses = {}

    def startProcess(self, name):
        """
        If possible, starts a new process.
        
        Args:
            process (Process): An instance of a Process class or child classes.
        """
        # Check if given process is not already running
        if self.runningProcesses[name] == None or not self.runningProcesses[name].is_alive():

            # Process was never started so start
            print('Starting process...')
            self.runningProcesses[name] = Process(target=self.assignedProcesses[name].run)
            self.runningProcesses[name].start()

        else:
            print('Nothing to do...')

    def stopProcess(self, process):
        """
        If possible, stops a running process.
        
        Args:
            process (Process): An instance of a Process class or child classes.
        """
        # Check if assigned processes are not already running
        if process.is_alive():

            # Stop process and release memory space associated
            print('Stopping process...')
            process.join()
            process.close()

        else:
            print('Nothing to do...')

    def assignProcess(self, name, process):
        """
        Method which allows assigning process to the supervisor.
        
        Args:
            name (String): An unique identifier for the process.
            process (Process): An instance of a Process class or child classes.
        """
        self.assignedProcesses[name] = process
        self.runningProcesses[name] = None

    def run(self):
        """
        The supervisor process starts all its assigned processes 
        as its children and monitors their work.
        """
        while True:

            print('Starting Assigned Processes:')

            # Start all assigned processes
            for name in self.assignedProcesses.keys():
                self.startProcess(name)

            # Check if processes are running every 10 sec
            time.sleep(10)