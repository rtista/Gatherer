# Own Imports
from model import Supervisor
from consumer import CustomConsumer

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
    
    # Create Consumer Instances
    custom1 = CustomConsumer('/queue/sigapabinho', stompconf, 
    {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL, StompSpec.ID_HEADER: 'consumer1'})
    custom2 = CustomConsumer('/queue/sigapabinho', stompconf, 
    {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL, StompSpec.ID_HEADER: 'consumer2'})
    custom3 = CustomConsumer('/queue/sigapabinho', stompconf, 
    {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL, StompSpec.ID_HEADER: 'consumer3'})
    custom4 = CustomConsumer('/queue/sigapabinho', stompconf, 
    {StompSpec.ACK_HEADER: StompSpec.ACK_CLIENT_INDIVIDUAL, StompSpec.ID_HEADER: 'consumer4'})

    # Create Supervisor
    supervisor = Supervisor()

    # Assign Consumers
    supervisor.assignConsumer(custom1)
    supervisor.assignConsumer(custom2)
    supervisor.assignConsumer(custom3)
    supervisor.assignConsumer(custom4)

    # Start the supervisor process
    supervisor.start()

    while True:
        print('boas')
        time.sleep(5)