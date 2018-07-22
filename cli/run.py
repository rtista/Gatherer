# Own Imports
from domain import Supervisor
from consumers import CustomConsumer

# Third Party Imports
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync import Stomp
import os
import time

# Stomp Connection Configuration
stompconf = StompConfig('tcp://127.0.0.1:61613', version='1.2')

# Mainn Loop
if __name__ == '__main__':

    # Create Supervisor
    supervisor = Supervisor()

    # Create Consumers
    consumer1 = CustomConsumer('/queue/sigapabinho', stompconf, 'consumer1')
    consumer2 = CustomConsumer('/queue/sigapabinho', stompconf, 'consumer2')
    consumer3 = CustomConsumer('/queue/sigapabinho', stompconf, 'consumer3')
    consumer4 = CustomConsumer('/queue/sigapabinho', stompconf, 'consumer4')

    # Assign Consumers
    supervisor.assignConsumer(consumer1)
    supervisor.assignConsumer(consumer2)
    supervisor.assignConsumer(consumer3)
    supervisor.assignConsumer(consumer4)

    # Start the supervisor process
    supervisor.start()