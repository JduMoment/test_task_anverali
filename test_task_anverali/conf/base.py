import os


class BaseConfig:
    NODE_ENV = os.getenv('NODE_ENV', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    DEBUG = False

    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///mydatabase.db'

    SENTRY_ENABLED = os.environ.get('SENTRY_ENABLED') == 'True'
    SENTRY_SDK_DNS = os.environ.get('SENTRY_SDK_DNS')

    OPEN_SEARCH_ENABLED = os.environ.get('OPEN_SEARCH_ENABLED') == 'True'
    OPEN_SEARCH_URL = os.environ.get('OPEN_SEARCH_URLz')
