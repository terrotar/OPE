# import app
from flask import Flask

from .blueprints.home import home
from .blueprints.login import login
from .blueprints.register import register

import config


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(register)

    return app
