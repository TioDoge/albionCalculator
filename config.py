from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config:
    SECRET_KEY                      = getenv('SECRET_KEY')
    TESTING                         = getenv('TESTING')
    
    PROPAGATE_EXCEPTIONS            = True
    ERROR_404_HELP                  = False
    
    # Data Base
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SHOW_SQLALCHEMY_LOG_MESSAGES    = False
    SQLALCHEMY_ECHO                 = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI         = getenv('SQLALCHEMY_DATABASE_URI_LOCAL')

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI         = getenv('SQLALCHEMY_DATABASE_URI')