from app import app

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db_teste/sqlite_therapies.db"
app.config['SECRET_KEY'] = "f1S\xbd\xb4cK/\xf4\x11\x0f\xc7f\xda7@"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
