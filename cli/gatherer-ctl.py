#!.venv/bin/python3

# Batteries
from sys import argv
from os import kill
from signal import SIGTERM
from argparse import ArgumentParser
from multiprocessing.connection import Client
    
# Own Imports
from supervisor import ConsumerSupervisor
from consume import CustomConsumer
from config import AppConfig


# Assigned Consumers Map (Class : count)
ASSIGNED_CONSUMERS = {
    CustomConsumer : 2,
}


def stop():
    '''
    Stops the gatherer-cli supervisor process.
    '''
    # Read Supervisor PID from pidfile
    try:
        with open(AppConfig.PID_LOCATION, 'r') as pidfile:
            pid = int(pidfile.readline())

        # Try to kill process
        kill(pid, SIGTERM)

    except FileNotFoundError:
        print('Could not find the {} file.'.format(AppConfig.PID_LOCATION))

    except ProcessLookupError:
        print('Could not find a process with the given PID. Stale PID file?')


def start():
    '''
    Starts the gatherer-cli supervisor process.
    '''
    # Create Supervisor
    supervisor = ConsumerSupervisor(ASSIGNED_CONSUMERS)

    # Start the supervisor process
    supervisor.start()


def restart():
    '''
    Restarts the gatherer-cli supervisor process.
    '''
    stop()
    start()


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
    'spawn': spawn
}


# Main
if __name__ == '__main__':

    # Create parser
    parser = ArgumentParser('gatherer-ctl')
    parser.add_argument('operation', type=str, choices=OPERATIONS.keys(), help='The operation to perform.')
    parser.add_argument('consumer', type=str, const=None, nargs='?', help='The name of the consumer to spawn/despawn.')
    parser.add_argument('dif', type=int, const=0, nargs='?', help='The number of consumers to spawn/despawn.')

    # Parser arguments
    args = parser.parse_args()
    
    # Check if simple operation
    if args.operation in ('stop', 'start', 'restart'):
        OPERATIONS[args.operation]()
        
    # Check for parameterized operation
    else:
        OPERATIONS[args.operation](args.consumer, args.dif)
