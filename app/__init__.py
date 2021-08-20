# import app
from flask import Flask

from .blueprints.home.routes import home


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home)

    return app
