from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_migrate import Migrate


db = SQLAlchemy(session_options={"autoflush": False})

login_manager = LoginManager()

migrate = Migrate()

UPLOAD_FOLDER = 'app/static/img'
