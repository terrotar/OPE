# import app
from flask import Flask

from app.config import db, login_manager, migrate, UPLOAD_FOLDER

from app.blueprints.home.routes import home
from app.blueprints.register.routes import register
from app.blueprints.login.routes import login
from app.blueprints.admin.routes import admin

from app.models.user import User
from app.models.product import Product
from app.models.therapy import Therapy
from app.models.cart_therapy import Cart_Therapy
from app.models.cart_product import Cart_Product
from app.models.order import Order


def create_app(config):
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql://postgres:postgres@localhost/TCC"
    app.config['SECRET_KEY'] = "f1S\xbd\xb4cK/\xf4\x11\x0f\xc7f\xda7@"
    app.secret_key = "\xc8\n~R\xae\xe3\xaao~\xb8E\x0fw\xc99"

    db.init_app(app)

    # Blueprints
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(register)
    app.register_blueprint(admin)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
