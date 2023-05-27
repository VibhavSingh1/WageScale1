import os
import flaskr.definitions as constants


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mysecretkey"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myapp.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Log config
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "default",
                "filename": constants.APP_LOG_FILE_PATH,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
            },
        },
        "root": {"level": "INFO", "handlers": ["file_handler"]},
    }
    # Celery-related app config
    CELERY_BROKER_URL = 'amqp://localhost'
    CELERY_RESULT_BACKEND = 'rpc://'


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "default",
                "filename": constants.APP_LOG_FILE_PATH,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
            },
        },
        "root": {"level": "DEBUG", "handlers": ["file_handler"]},
    }


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
