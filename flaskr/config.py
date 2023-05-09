import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mysecretkey"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myapp.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
