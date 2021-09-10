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
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column("id_usuario", db.Integer, primary_key=True)
    __email = db.Column("email", db.String, unique=True, nullable=False)
    __password = db.Column("senha", db.String, nullable=False)
    __cpf = db.Column("cpf", db.BigInteger, unique=True, nullable=False)
    __cep = db.Column("cep", db.String, unique=False, nullable=False)
    __address = db.Column("endereco", db.String, unique=False, nullable=False)
    __number = db.Column("numero", db.String, unique=False, nullable=False)
    __uf = db.Column("uf", db.String, unique=False, nullable=False)
    __city = db.Column("cidade", db.String, unique=False, nullable=False)
    __complement = db.Column("complemento", db.String, unique=False, nullable=True)
    __fname = db.Column("nome", db.String, unique=False, nullable=False)
    __lname = db.Column("sobrenome", db.String, unique=False, nullable=False)
    __birthday = db.Column("nascimento", db.Date, unique=False, nullable=False)
    __age = db.Column("idade", db.Integer, unique=False, nullable=True)

    # When create a new User object, you must use the following functions:

    # check_age() --> Validates if user can purchase items or not
    # check_cpf() --> Validates the cpf format when user register a new account
    # set_adress() --> Get the adress via API and set in user attributes
    def __init__(self, email, password, cpf, cep, number, complement, fname, lname, birthday):
        self.__email = email
        self.__password = generate_password_hash(password)
        # cpf cant be masked already(cpf.mask(cpf_to_mask))
        # it can be like "12345678910" or 12345678910
        # Although, the mapped is set to be Integer
        self.__cpf = cpf
        # Create cpf that verify name
        self.__cep = cep
        self.__number = number
        self.__complement = complement
        self.__fname = fname
        self.__lname = lname
        self.__birthday = birthday

    # VALIDATORS
    # Age must be >= 18 to purchase items
    def check_age(self):
        today = datetime.date.today()
        days = today - self.__birthday
        age = int(days.days)//365
        if age >= 18:
            return True
        else:
            return False

    # Cpf must be validated with it's rules
    def check_cpf(self):
        num = cpf.mask(str(self.__cpf))
        return cpf.validate(num)

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

    # Cpf
    @hybrid_property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    # Cep
    @hybrid_property
    def cep(self):
        return self.__cep

    @cep.setter
    def cep(self, cep):
        self.__cep = cep

    # Number
    @hybrid_property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    # Adress
    @hybrid_property
    def address(self):
        return self.__address

    def set_address(self):
        address = requests.get(f"https://viacep.com.br/ws/{self.__cep}/json/")
        self.__address = address.json()["logradouro"]
        self.__uf = address.json()["uf"]
        self.__city = address.json()["localidade"]

    # UF
    @hybrid_property
    def uf(self):
        return self.__uf

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

    # Complement
    @hybrid_property
    def complement(self):
        return self.__complement

    @complement.setter
    def complement(self, complement):
        self.__complement = complement

    # Age
    @hybrid_property
    def age(self):
        return self.__age

    def set_age(self):
        today = datetime.date.today()
        days = today - self.__birthday
        age = int(days.days)//365
        self.__age = age
