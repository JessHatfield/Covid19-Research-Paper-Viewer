import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# This gives us the root directory of the project
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.getcwd(), 'api.db')}"
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN="http://127.0.0.1:5000"
