from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from search_api.config import Config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    from search_api.app.routes import bp as route_bp
    app.register_blueprint(route_bp, url_prefix='/api/v1')

    return app


app = create_app(config_class=Config)
