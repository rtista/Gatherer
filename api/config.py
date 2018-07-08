class Config:
    '''
    Configuration class to hold all configurations for the API.
    '''
    # Application name
    APP_NAME = 'Gatherer API'

    # Debugging Mode
    DEBUG = True

    # Server listening config
    SERVER = {
        'url': '127.0.0.1',
        'port': '8000'
    }

    # ActiveMQ connection configuration
    ACTIVEMQ = {
        'url': '127.0.0.1',
        'port': 1234,
    }


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
