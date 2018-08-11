# Third-party Imports
from threading import Thread


class UnixListener(Thread):
    """    
    A UNIX_AF socket listener which listens for
    commands from another process.
    
    Args:
        Thread (threading.Thread): Extends the Thread class for asychronous execution.
    """
    def __init__(self, sock, monitormap):
        """
        Creates the object.
        
        Args:
            sock (multiprocessing.connection.Listener): The Listener object.
            monitormap (dict): The mapping of consumers to monitored count.
        """
        Thread.__init__(self)
        self.sock = sock
        self.monitormap = monitormap

    def run(self):
        """
        Listens for commands from a unix_af listener.s
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
                    for elem in self.monitormap.keys():
                        if elem.__name__ == op[1]:
                            self.monitormap[elem] += int(op[2])