# Application environment definition
# env = os.environ['APPLICATION_ENV']
env = 'development'

if env == 'development':
    from .config import DevelopmentConfig as AppConfig
elif env == 'staging':
    from .config import StagingConfig as AppConfig
elif env == 'production':
    from .config import ProductionConfig as AppConfig
else:
    raise ValueError('Invalid environment')