import os


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:PIANO@230jap@localhost/depths_char_sheet_2'


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('HEROKU_POSTGRESQL_GREEN_URL')


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:PIANO@230jap@localhost/depths-char-staging'
