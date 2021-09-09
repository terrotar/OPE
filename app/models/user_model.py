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
    __tablename__ = "usuario"
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    _email = db.Column("email", db.String, unique=True, nullable=False)
    _password = db.Column("senha", db.String, nullable=False)
    _cpf = db.Column("cpf", db.BigInteger, unique=True, nullable=False)
    _cep = db.Column("cep", db.String, unique=False, nullable=False)
    _address = db.Column("endereco", db.String, unique=False, nullable=False)
    _number = db.Column("numero", db.String, unique=False, nullable=False)
    _uf = db.Column("uf", db.String, unique=False, nullable=False)
    _city = db.Column("cidade", db.String, unique=False, nullable=False)
    _complement = db.Column("complemento", db.String, unique=False, nullable=True)
    _fname = db.Column("nome", db.String, unique=False, nullable=False)
    _lname = db.Column("sobrenome", db.String, unique=False, nullable=False)
    _birthday = db.Column("nascimento", db.Date, unique=False, nullable=False)
    _age = db.Column("idade", db.Integer, unique=False, nullable=True)

    # When create a new User object, you must use the following functions:

    # check_age() --> Validates if user can purchase items or not
    # check_cpf() --> Validates the cpf format when user register a new account
    # set_adress() --> Get the adress via API and set in user attributes
    def __init__(self, email, password, cpf, cep, number, complement, fname, lname, birthday):
        self._email = email
        self._password = generate_password_hash(password)
        # cpf cant be masked already(cpf.mask(cpf_to_mask))
        # it can be like "12345678910" or 12345678910
        # Although, the mapped is set to be Integer
        self._cpf = cpf
        # Create cpf that verify name
        self._cep = cep
        self._number = number
        self._complement = complement
        self._fname = fname
        self._lname = lname
        self._birthday = birthday

    # VALIDATORS
    # Age must be >= 18 to purchase items
    def check_age(self):
        today = datetime.date.today()
        days = today - self._birthday
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

    # Number
    @hybrid_property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    # Adress
    @hybrid_property
    def address(self):
        return self._address

    def set_address(self):
        address = requests.get(f"https://viacep.com.br/ws/{self._cep}/json/")
        self._address = address.json()["logradouro"]
        self._uf = address.json()["uf"]
        self._city = address.json()["localidade"]

    # UF
    @hybrid_property
    def uf(self):
        return self._uf

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

    # Complement
    @hybrid_property
    def complement(self):
        return self._complement

    @complement.setter
    def complement(self, complement):
        self._complement = complement

    # Age
    @hybrid_property
    def age(self):
        return self._age

    def set_age(self):
        today = datetime.date.today()
        days = today - self._birthday
        age = int(days.days)//365
        self._age = age
