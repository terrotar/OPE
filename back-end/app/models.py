from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import requests


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column("email", db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    _cpf = db.Column("cpf", db.Integer, unique=True, nullable=False)
    _cep = db.Column("cep", db.Integer, unique=False, nullable=False)
    _adress = db.Column("adress", db.String, unique=False, nullable=False)
    _uf = db.Column("uf", db.String, unique=False, nullable=False)
    _complement = db.Column("complement", db.String, unique=False, nullable=True)
    _name = db.Column("name", db.String, unique=False, nullable=False)
    # Nedd to create age attribute

    def __init__(self, email, password, cpf, cep, complement, name):
        self._email = email
        self._password = generate_password_hash(password)
        self._cpf = cpf
        # Create cpf that verify name
        self._cep = cep
        self._complement = complement
        self._name = name

    # Properties of GET and SET
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

    # Cpf
    @hybrid_property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    #Cep
    @hybrid_property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, cep):
        self._cep = cep

    # Adress
    @hybrid_property
    def adress(self):
        return self._adress

    def set_adress(self, cep):
        adress = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        self._adress = adress.json()["logradouro"]
        self._uf = adress.json()["uf"]

    # UF
    @hybrid_property
    def uf(self):
        return self._uf

    # Name
    @hybrid_property
    def name(self):
        return self._name

    # Complement
    def complement(self):
        return self._complement


db.create_all()
