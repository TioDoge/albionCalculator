from app import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()

if getenv('FLASK_ENV') == 'development':
    settings = 'config.DevConfig'
else:
    settings = 'config.ProdConfig'

app = create_app(settings)