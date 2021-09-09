from app.config import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


# Login functions
@login_manager.user_loader
def get_user(user_id):
    return Admin.query.filter_by(id=user_id).first()


# Columns of table funcionario
class Admin(db.Model, UserMixin):
    __tablename__ = "funcionario"
    id_funcionario = db.Column("id_funcionario", db.Integer, primary_key=True)
    _email = db.Column("email", db.String, unique=True, nullable=False)
    _password = db.Column("senha", db.String, nullable=False)
    _fname = db.Column("nome", db.String, unique=False, nullable=False)
    _lname = db.Column("sobrenome", db.String, unique=False, nullable=False)

    def __init__(self, email, password, fname, lname):
        self._email = email
        self._password = generate_password_hash(password)
        self._fname = fname
        self._lname = lname

# PROPERTIES of GET and SET attributes
    # Email

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    # Password
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    # Verify the hash password
    def verify_password(self, pwd):
        return check_password_hash(self._password, pwd)

    # Fname
    @hybrid_property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, fname):
        self._fname = fname

    # Lname
    @hybrid_property
    def lname(self):
        return self._lname

    @lname.setter
    def lname(self, lname):
        self._lname = lname
