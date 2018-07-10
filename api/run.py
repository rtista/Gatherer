#!/usr/bin/env python3

# Own Imports
from middleware import ActiveMQSession
from resources import CollectorIdResource
from config import AppConfig

# Third-party Imports
from stompest.config import StompConfig
from stompest.sync import Stomp

# import os
import falcon
import bjoern

###########################################
# ActiveMQ Stomp Connection Configuration #
###########################################
stompconf = StompConfig('tcp://{}:{}'.format(AppConfig.ACTIVEMQ['host'], AppConfig.ACTIVEMQ['port']),
                        login=AppConfig.ACTIVEMQ['user'],
                        passcode=AppConfig.ACTIVEMQ['pass'],
                        version=AppConfig.ACTIVEMQ['stomp_version'])

############################
# Falcon API Configuration #
############################

# Middleware Configuration
api = falcon.API(
        middleware=[
            ActiveMQSession(stompconf)
        ]
    )

# Route Configuration
api.add_route('/collector/{queue}', CollectorIdResource())

# Serve application
if __name__ == '__main__':

    bjoern.listen(api, AppConfig.SERVER['url'], AppConfig.SERVER['port'])
    bjoern.run()
