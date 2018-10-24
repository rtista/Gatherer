# Own Imports
from signal import signal
from multiprocessing import Process


class UnixProcess(Process):
    """
    A Unix Process is capable of handling kill signals
    with the associated handler functions.
    """

    def __init__(self, name):
        """
        Create a new Unix Process class instance.

        Args:
            name (str): The process name.
        """
        Process.__init__(self, name=name)
        self.sigmap = {}

    def addSighandler(self, sig, sighandler):
        """
        Allows adding handler functions for unix signals.

        Args:
            sig (int): The signal to be handled.
            sighandler (function): The handler function.
        """
        self.sigmap[sig] = sighandler

    def mapSignalHandlers(self):
        """
        Registers the associated signal handlers.
        """
        for key in self.sigmap:
            signal(key, self.sigmap[key])
