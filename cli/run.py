# Own Imports
from consume import CustomConsumer
from supervisor import ConsumerSupervisor
from config import AppConfig

# Third Party Imports
from stompest.config import StompConfig
from stompest.protocol import StompSpec
from stompest.sync import Stomp
import os
import time


# Stomp Connection Configuration
stompconf = StompConfig('tcp://{}:{}'.format(AppConfig.ACTIVEMQ['host'], AppConfig.ACTIVEMQ['port']),
                         version=AppConfig.ACTIVEMQ['stomp_version'])

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