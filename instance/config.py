import os

base_dir = os.path.abspath(os.path.dirname(__file__))

# Base configuration
class Config(object):
    DEBUG = False
    SECRET = os.getenv('STOREMANAGER_SECRET', 'DoNotTellPeopleYourSecrets')
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_USER = os.getenv("DATABASE_USER", "store")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "123store")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "storemanager")


# Dev configuration
class DevConfig(Config):
    DEBUG = True


# Test configuration
class TestConfig(Config):
    TESTING = True
    DEBUG = True


# Staging configuration
class StagingConfig(Config):
    DEBUG = True


# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False