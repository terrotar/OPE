from app.config import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import requests
import datetime
from validate_docbr import CPF


# class from package validate_docbr to validate the docs
cpf = CPF()


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column("email", db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    _cpf = db.Column("cpf", db.BigInteger, unique=True, nullable=False)
    _cep = db.Column("cep", db.String, unique=False, nullable=False)
    _address = db.Column("address", db.String, unique=False, nullable=False)
    _uf = db.Column("uf", db.String, unique=False, nullable=False)
    _complement = db.Column("complement", db.String, unique=False, nullable=True)
    _name = db.Column("name", db.String, unique=False, nullable=False)
    _bday = db.Column("bday", db.Integer, unique=False, nullable=False)
    _bmonth = db.Column("bmonth", db.Integer, unique=False, nullable=False)
    _byear = db.Column("byear", db.Integer, unique=False, nullable=False)

    # When create a new User object, you must use the following functions:

    # check_age() --> Validates if user can purchase items or not
    # check_cpf() --> Validates the cpf format when user register a new account
    # set_adress() --> Get the adress via API and set in user attributes
    def __init__(self, email, password, cpf, cep, complement, name, bday, bmonth, byear):
        self._email = email
        self._password = generate_password_hash(password)
        # cpf cant be masked already(cpf.mask(cpf_to_mask))
        # it can be like "12345678910" or 12345678910
        # Although, the mapped is set to be Integer
        self._cpf = cpf
        # Create cpf that verify name
        self._cep = cep
        self._complement = complement
        self._name = name
        self._bday = bday
        self._bmonth = bmonth
        self._byear = byear

    # VALIDATORS
    # Age must be >= 18 to purchase items
    def check_age(self):
        today = datetime.date.today()
        birth = datetime.date(self._byear, self._bmonth, self._bday)
        days = today - birth
        age = int(days.days)//365
        if age >= 18:
            return True
        else:
            return False

    # Cpf must be validated with it's rules
    def check_cpf(self):
        num = cpf.mask(str(self._cpf))
        return cpf.validate(num)

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

    # Cpf
    @hybrid_property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    # Cep
    @hybrid_property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, cep):
        self._cep = cep

    # Adress
    @hybrid_property
    def address(self):
        return self._address

    def set_address(self):
        address = requests.get(f"https://viacep.com.br/ws/{self._cep}/json/")
        self._address = address.json()["logradouro"]
        self._uf = address.json()["uf"]

    # UF
    @hybrid_property
    def uf(self):
        return self._uf

    # Name
    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    # Complement
    @hybrid_property
    def complement(self):
        return self._complement

    @complement.setter
    def complement(self, complement):
        self._complement = complement

    # Bday, bmonth and byear
    @hybrid_property
    def bday(self):
        return self._bday

    @hybrid_property
    def bmonth(self):
        return self._bmonth

    @hybrid_property
    def byear(self):
        return self._byear
