# Own Imports
from consume import CustomConsumer
from supervisor import ConsumerSupervisor

# Third Party Imports
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync import Stomp
import os
import time

#test
from signal import signal, SIGTERM, SIGINT

# Stomp Connection Configuration
stompconf = StompConfig('tcp://127.0.0.1:61613', version='1.2')

# Main Loop
if __name__ == '__main__':

    # Create Supervisor
    supervisor = ConsumerSupervisor()

    # Create Consumers
    customConsumer = CustomConsumer('/queue/sigapabinho', stompconf)

    # Assign Consumers
    supervisor.assignConsumer('consumer1', customConsumer)
    supervisor.assignConsumer('consumer2', customConsumer)

    # Start the supervisor process
    supervisor.start()