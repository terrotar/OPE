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
    id = db.Column("id_funcionario", db.Integer, primary_key=True)
    __email = db.Column("email", db.String, unique=True, nullable=False)
    __password = db.Column("senha", db.String, nullable=False)
    __fname = db.Column("nome", db.String, unique=False, nullable=False)
    __lname = db.Column("sobrenome", db.String, unique=False, nullable=False)

    def __init__(self, email, password, fname, lname):
        self.__email = email
        self.__password = generate_password_hash(password)
        self.__fname = fname
        self.__lname = lname

# PROPERTIES of GET and SET attributes
    # Email

    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    # Password
    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = generate_password_hash(password)

    # Verify the hash password
    def verify_password(self, pwd):
        return check_password_hash(self.__password, pwd)

    # Fname
    @hybrid_property
    def fname(self):
        return self.__fname

    @fname.setter
    def fname(self, fname):
        self.__fname = fname

    # Lname
    @hybrid_property
    def lname(self):
        return self.__lname

    @lname.setter
    def lname(self, lname):
        self.__lname = lname
