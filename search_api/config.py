import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(os.getcwd(), 'api.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_DOMAIN="http://127.0.0.1:5000"
