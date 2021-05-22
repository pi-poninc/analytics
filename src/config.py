import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    API_KEY = os.getenv('environment variables') or 'Please put your parameter'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
    }
