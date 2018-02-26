import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PLAID_CLIENT_ID = os.environ['PLAID_CLIENT_ID']
    PLAID_SECRET = os.environ['PLAID_SECRET']
    PLAID_PUBLIC_KEY = os.environ['PLAID_PUBLIC_KEY']


class ProductionConfig(Config):
    DEBUG = False
    PLAID_ENV = 'production'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    PLAID_ENV = 'staging'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    PLAID_ENV = 'development'


class TestingConfig(Config):
    TESTING = True
    PLAID_ENV = 'testing'
