from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

from flask_migrate import Migrate


db = SQLAlchemy(session_options={"autoflush": False})

login_manager = LoginManager()

migrate = Migrate()

UPLOAD_FOLDER = 'app/static/img'

# app.config['SQLALCHEMY_DATABASE_URL'] = "postgresql://postgres:postgres@localhost/TCC"
DATABASE_URI = 'postgresql://drzqvuvqbehtlc:975200bfaaca476937e61bfc1cf315e9f5a11e326c11c068ec2400754a8b9b0d@ec2-3-89-214-80.compute-1.amazonaws.com:5432/dep7ghagq8oere'
