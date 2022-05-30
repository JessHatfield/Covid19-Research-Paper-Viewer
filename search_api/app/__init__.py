from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from search_api.config import Config


def create_app(config_class=Config):
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config.from_object()
    db.init_app(app)
    return app
