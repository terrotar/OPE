# import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db_teste/sqlite_therapies.db"


login_manager = LoginManager(app)


db = SQLAlchemy(app)
