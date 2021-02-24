from os import environ, path
from dotenv import load_dotenv
import string
import random

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(12))


class Config:

    # Server
    SERVER_PORT = environ.get("SERVER_PORT")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = key
