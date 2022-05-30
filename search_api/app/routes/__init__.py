from flask import Blueprint

bp = Blueprint('main', __name__)

from search_api.app.routes import routes
