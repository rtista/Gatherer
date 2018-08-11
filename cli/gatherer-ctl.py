#!.venv/bin/python3

# Own Imports
from supervisor import ConsumerSupervisor
from consume import CustomConsumer
from config import AppConfig

# Third-party Imports
from sys import argv
from os import kill
from signal import SIGTERM
from multiprocessing.connection import Client


# Assigned Consumers Map (Class : count)
ASSIGNED_CONSUMERS = {
    CustomConsumer : 2,
}


def stop():
    '''
    Stops the gatherer-cli supervisor process.
    '''
    pid = None

    try:
        with open(AppConfig.PID_LOCATION, 'r') as pidfile:
            pid = int(pidfile.readline())

    except FileNotFoundError:
        print('Could not find the {} file.'.format(AppConfig.PID_LOCATION))
        exit(1)

    if pid is not None:

        # Try to kill process
        try:
            kill(pid, SIGTERM)

        except ProcessLookupError:
            print('Could not find a process with the given PID. Stale PID file?')
            exit(1)


def start():
    '''
    Starts the gatherer-cli supervisor process.
    '''
    # Create Supervisor
    supervisor = ConsumerSupervisor()

    # Assign Consumers
    for consumer in ASSIGNED_CONSUMERS.keys():
        supervisor.assignConsumer(consumer, ASSIGNED_CONSUMERS[consumer])

    # Start the supervisor process
    supervisor.start()


def restart():
    '''
    Restarts the gatherer-cli supervisor process.
    '''
    stop()
    start()


def startConsumer(consumer):
    '''
    Start the consumers of the given class.
    
    Args:
        args (list): Arguments to be passed onto the function.
    '''
    raise NotImplementedError('Not yet implemented')


def stopConsumer(consumer):
    '''
    Stops all the consumers of the given class.
    
    Args:
        args (list): Arguments to be passed onto the function.
    '''
    raise NotImplementedError('Not yet implemented')


def spawn(consumer, dif):
    '''
    Spawns or reduces the number of monitored consumers.
    
    Args:
        args (list): Arguments to be passed onto the function.
    '''
    client = Client(AppConfig.UNIX_SOCKET, 'UNIX_AF')

    client.send(['spawn', consumer, dif])

    client.close()


# Available operations
OPERATIONS = {
    'stop': stop,
    'start': start,
    # 'reload': reload,
    'restart': restart,
    'consumer': {
        'start': startConsumer,
        'stop': stopConsumer,
        'spawn': spawn,
    }
}


# Main
if __name__ == '__main__':

    print('argv: {}'.format(argv))

    arglen = len(argv)
    
    if arglen == 2: 
        OPERATIONS[argv[1]]()
    
    elif arglen == 4: 
        OPERATIONS[argv[1]][argv[2]](argv[3])
    
    elif arglen == 5:
        OPERATIONS[argv[1]][argv[2]](argv[3], argv[4])
    
    else:
        print('Missing')
