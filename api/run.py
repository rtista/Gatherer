#!/usr/bin/env python3

# Own Imports
from .middleware import ActiveMQSession
from .resources import CollectorIdResource
from .config import DevelopmentConfig, StagingConfig, ProductionConfig

# Third-party Imports
# import os
import stomp
import falcon
import bjoern

# Application environment definition
# env = os.environ['APPLICATION_ENV']
env = 'development'

if env == 'development':
    app_config = DevelopmentConfig
elif env == 'staging':
    app_config = StagingConfig
elif env == 'production':
    app_config = ProductionConfig
else:
    raise ValueError('Invalid environment')

#####################################
# ActiveMQ Connection Configuration #
#####################################
# TODO: Start stomp connection

############################
# Falcon API Configuration #
############################

# Middleware Configuration
# TODO Add ActiveMQSession middleware
api = falcon.API(
        middleware=[
            
        ]
    )

# Route Configuration
api.add_route('/collector/{queue:str}', CollectorIdResource())

# Serve application
if __name__ == '__main__':

    bjoern.listen(api, app_config.SERVER['url'], app_config.SERVER['port'])
    bjoern.run()

# TODO: Shutdown ActiveMQ connection