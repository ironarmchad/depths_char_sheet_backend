import os

# uncomment the line below for postgres database url from environment variable

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'o\xec\xea\xc6\xe0\xda\x1dZ5\x07\xb2\\\xeb\xf6{:'
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:PIANO@230jap@localhost/depths_char_sheet_2'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

