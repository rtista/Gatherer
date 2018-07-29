class Config:
    '''
    Configuration class to hold all configurations for the CLI.
    '''
    # Application name
    APP_NAME = 'Gatherer CLI'

    # ActiveMQ connection configuration
    ACTIVEMQ = {
        'host': 'url',
        'port': 11111,
        'stomp_version': '1.2'
    }

    # PID File Location
    PID_LOCATION = './gatherer-cli.pid'

class DevelopmentConfig(Config):
    '''
    Configuration for the development environment.
    '''
    # Debugging Mode
    DEBUG = True

class StagingConfig(Config):
    '''
    Configuration for the staging environment.
    '''
    # Debugging Mode
    DEBUG = True


class ProductionConfig(Config):
    '''
    Configuration for the production environment.
    '''
    # Debugging Mode
    DEBUG = False
