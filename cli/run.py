# Own Imports
from supervisor import ConsumerSupervisor
from consume import CustomConsumer
from config import AppConfig


# Assigned Consumers Map (Class : count)
ASSIGNED_CONSUMERS = {
    CustomConsumer : 2,
}


# Main Loop
if __name__ == '__main__':

    # Create Supervisor
    supervisor = ConsumerSupervisor()

    # Assign Consumers
    for consumer in ASSIGNED_CONSUMERS.keys():
        supervisor.assignConsumer(consumer, ASSIGNED_CONSUMERS[consumer])

    # Start the supervisor process
    supervisor.start()