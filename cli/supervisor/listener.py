# Third-party Imports
from threading import Thread


class UnixListener(Thread):
    """    
    A UNIX_AF socket listener which listens for
    commands from another process.
    
    Args:
        Thread (threading.Thread): Extends the Thread class for asychronous execution.
    """
    def __init__(self, sock, children):
        """
        Creates the object.
        
        Args:
            sock (multiprocessing.connection.Listener): The Listener object.
            children (dict): The mapping of the supervisor assigned processes.
        """
        Thread.__init__(self)
        self.sock = sock
        self.children = children

    def spawnProcess(self, process, dif):
        """
        Starts a process if not running.
        
        Args:
            process (str): The name of the process to start.
            dif (int): Number of instances of the process to spawn.
        """
        # Fail if process not in
        if process not in self.children.keys():
            return
        
        self.children[process]['monitored'] += dif

        if self.children[process]['monitored'] < 0:
            self.children[process]['monitored'] = 0

    def stopProcess(self, process):
        """
        Stops all instances of a process.
        
        Args:
            process (str): The name of the process to start.
        """
        if process not in self.children.keys():
            return

        self.children[process]['monitored'] = 0

    def run(self):
        """
        Listens for commands from a UNIX_AF listener.
        """
        # Endless Loop
        while True:

            # Locks until connection
            with self.sock.accept() as connection:

                # Check if there is content to be read
                if connection.poll(timeout=1.0):

                    # Reads content from socket
                    op = connection.recv()
                    
                    # Action
                    if op[0] == 'spawn':
                        self.spawnProcess(op[1], int(op[2]))
                        
                    elif op[0] == 'stop':
                        self.stopProcess(op[1])
