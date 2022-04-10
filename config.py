""" Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    SECRET_KEY = 'SECRET_KEY'
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # MariaDB Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'ehfleet'
    MYSQL_PASSWORD = '_EHFleet_'
    MYSQL_DB = 'dlc'
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ehfleet:_EHFleet_@localhost/dlc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
